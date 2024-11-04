# pylint: disable=W0105, W0107, R1705, R1723, R0914

import json
import os
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from time import sleep
from typing import Dict, Optional

import boto3


class DataSourceType(Enum):
    AWS_LAMBDA = "AWS_LAMBDA"
    AMAZON_DYNAMODB = "AMAZON_DYNAMODB"
    AMAZON_ELASTICSEARCH = "AMAZON_ELASTICSEARCH"
    NONE = "NONE"
    HTTP = "HTTP"
    RELATIONAL_DATABASE = "RELATIONAL_DATABASE"
    AMAZON_OPENSEARCH_SERVICE = "AMAZON_OPENSEARCH_SERVICE"


class AuthenticationType(Enum):
    API_KEY = "API_KEY"
    AWS_IAM = "AWS_IAM"
    AMAZON_COGNITO_USER_POOLS = "AMAZON_COGNITO_USER_POOLS"
    OPENID_CONNECT = "OPENID_CONNECT"
    AWS_LAMBDA = "AWS_LAMBDA"


@dataclass
class DataSourceDTO:
    api_id: str
    name: str
    data_source_type: DataSourceType
    serviceRoleArn: Optional[str] = None
    description: Optional[str] = ""
    config: Optional[Dict] = None


@dataclass
class GraphQLAPIDTO:
    api_name: str
    region: str
    authentication_type: AuthenticationType
    logs_config: Dict
    user_pool_config: Optional[Dict] = None
    open_id_connect_config: Optional[Dict] = None
    lambda_authorizer_config: Optional[Dict] = None
    api_key_expires_in_seconds: Optional[int] = 604800  # 1 Week


@dataclass
class ResolverDTO:
    api_id: str
    type_name: str
    field_name: str
    data_source_name: str
    kind: Optional[str] = "UNIT"
    request_mapping_template: Optional[str] = None
    response_mapping_template: Optional[str] = None
    pipeline_config: Optional[Dict] = None
    sync_config: Optional[Dict] = None
    caching_config: Optional[Dict] = None


@dataclass
class FunctionDTO:
    api_id: str
    name: str
    data_source_name: str
    description: Optional[str] = ""
    function_id: Optional[str] = None
    request_mapping_template: Optional[str] = None
    response_mapping_template: Optional[str] = None
    function_version: Optional[str] = "2018-05-29"
    sync_config: Optional[Dict] = None


@dataclass
class CacheDTO:
    api_id: str
    ttl: int
    apiCachingBehavior: str
    type: str
    transitEncryptionEnabled: Optional[bool] = False
    atRestEncryptionEnabled: Optional[bool] = False


app_sync_client = boto3.client("appsync", region_name="ap-south-1")
r_53_client = boto3.client("route53", region_name="ap-south-1")
iam_client = boto3.client("iam", region_name="ap-south-1")


def get_aws_account_id():
    client = boto3.client("sts")
    account_id = client.get_caller_identity()["Account"]

    return account_id


def get_lambda_func_arn(func_name, region):
    account_id = get_aws_account_id()

    arn = f"arn:aws:lambda:{region}:{account_id}:function:{func_name}"

    return arn


def get_api_details(api_name, authentication_type):
    #     graphql_apis = []
    nextToken = "init"

    while nextToken:
        if nextToken != "init":
            response = app_sync_client.list_graphql_apis(
                nextToken=nextToken, maxResults=25
            )
        else:
            response = app_sync_client.list_graphql_apis(maxResults=25)

        for api in response.get("graphqlApis", []):
            if api["name"] == api_name:
                return {"graphqlApi": api}

        #         graphql_apis.extend(response("graphqlApis", []))

        nextToken = response.get("nextToken")

    return


def create_api_key(api_id, expires_in_seconds):
    expires_in_seconds = int(datetime.now().timestamp() + expires_in_seconds)

    try:
        response = app_sync_client.create_api_key(
            apiId=api_id,
            description="API Key Description",
            expires=expires_in_seconds,
        )
    except Exception as e:
        return {"errors": str(e)}

    return response


def get_valid_api_keys_of_api(api_id):
    nextToken = "init"
    api_keys = []

    while nextToken:
        if nextToken != "init":
            response = app_sync_client.list_api_keys(
                apiId=api_id, nextToken=nextToken, maxResults=25
            )
        else:
            response = app_sync_client.list_api_keys(
                apiId=api_id, maxResults=25
            )

        api_keys.extend(
            [
                api_key
                for api_key in response["apiKeys"]
                if datetime.fromtimestamp(api_key["expires"]) > datetime.now()
            ]
        )
        nextToken = response.get("nextToken")

    return api_keys


def create_api_cache(cache_dto: CacheDTO):
    try:
        response = app_sync_client.create_api_cache(
            apiId=cache_dto.api_id,
            ttl=cache_dto.ttl,
            transitEncryptionEnabled=cache_dto.transitEncryptionEnabled,
            atRestEncryptionEnabled=cache_dto.atRestEncryptionEnabled,
            apiCachingBehavior=cache_dto.apiCachingBehavior,
            type=cache_dto.type,
        )
    except Exception as e:
        return {"errors": str(e)}

    return response


def create_graphql_api(graphql_api_dto: GraphQLAPIDTO):
    params = {
        "name": graphql_api_dto.api_name,
        "authenticationType": graphql_api_dto.authentication_type,
    }

    if (
        graphql_api_dto.authentication_type
        == AuthenticationType.AWS_LAMBDA.value
    ):
        """
        lambdaAuthorizerConfig: {
            'authorizerResultTtlInSeconds': 123,
            'authorizerUri': 'string',
            'identityValidationExpression': 'string'
        }
        """
        params.update(
            {
                "lambdaAuthorizerConfig": graphql_api_dto.lambda_authorizer_config
            }
        )

    if (
        graphql_api_dto.authentication_type
        == AuthenticationType.AMAZON_COGNITO_USER_POOLS.value
    ):
        """
        userPoolConfig: {
            'userPoolId': 'string',
            'awsRegion': 'string',
            'defaultAction': 'ALLOW'|'DENY',
            'appIdClientRegex': 'string'
        }
        """

        params.update({"userPoolConfig": graphql_api_dto.user_pool_config})

    if (
        graphql_api_dto.authentication_type
        == AuthenticationType.OPENID_CONNECT.value
    ):
        """
        openIDConnectConfig: {
            'issuer': 'string',
            'clientId': 'string',
            'iatTTL': 123,
            'authTTL': 123
        }
        """

        params.update(
            {"openIDConnectConfig": graphql_api_dto.open_id_connect_config}
        )

    if graphql_api_dto.logs_config.get("enabled"):
        account_id = get_aws_account_id()

        cw_policy_statements = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ],
                    "Resource": [f"arn:aws:logs:ap-south-1:{account_id}:*"],
                }
            ],
        }

        assume_role_policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "appsync.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }

        service_role_name = (
            f"{graphql_api_dto.api_name}-appsync-graphqlapi-logs"[:64]
        )

        response = create_service_role(
            role_name=service_role_name, policy_doc=assume_role_policy_doc
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Service role for {graphql_api_dto.api_name} CW Logs "
                }
            )
            return response

        inline_policy_name = (
            f"{graphql_api_dto.api_name}-appsync-graphqlapi-cw-logs-access"[
                :128
            ]
        )

        response = put_inline_policy_to_role(
            role_name=service_role_name,
            policy_name=inline_policy_name,
            policy_doc=cw_policy_statements,
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Inline Policy for Service Role of  {graphql_api_dto.api_name} CW Logs"
                }
            )
            return response

        cw_service_role_arn = (
            f"arn:aws:iam::{account_id}:role/service-role/{service_role_name}"
        )

        logs_config = {
            "fieldLogLevel": graphql_api_dto.logs_config.get(
                "fieldLogLevel", "ERROR"
            ),
            "cloudWatchLogsRoleArn": cw_service_role_arn,
            "excludeVerboseContent": graphql_api_dto.logs_config.get(
                "excludeVerboseContent", True
            ),
        }

        params.update({"logConfig": logs_config})

    try:
        response = app_sync_client.create_graphql_api(**params)

    except Exception as e:
        response = {"errors": str(e)}

    return response


def update_authentication_type_of_graphql_api(api_id, graphql_api_dto):
    params = {
        "apiId": api_id,
        "name": graphql_api_dto.api_name,
        "authenticationType": graphql_api_dto.authentication_type,
    }

    if (
        graphql_api_dto.authentication_type
        == AuthenticationType.AWS_LAMBDA.value
    ):
        """
        lambdaAuthorizerConfig: {
            'authorizerResultTtlInSeconds': 123,
            'authorizerUri': 'string',
            'identityValidationExpression': 'string'
        }
        """
        params.update(
            {
                "lambdaAuthorizerConfig": graphql_api_dto.lambda_authorizer_config
            }
        )

    if (
        graphql_api_dto.authentication_type
        == AuthenticationType.AMAZON_COGNITO_USER_POOLS.value
    ):
        """
        userPoolConfig: {
            'userPoolId': 'string',
            'awsRegion': 'string',
            'defaultAction': 'ALLOW'|'DENY',
            'appIdClientRegex': 'string'
        }
        """

        params.update({"userPoolConfig": graphql_api_dto.user_pool_config})

    if (
        graphql_api_dto.authentication_type
        == AuthenticationType.OPENID_CONNECT.value
    ):
        """
        openIDConnectConfig: {
            'issuer': 'string',
            'clientId': 'string',
            'iatTTL': 123,
            'authTTL': 123
        }
        """

        params.update(
            {"openIDConnectConfig": graphql_api_dto.open_id_connect_config}
        )

    #  Logs

    if graphql_api_dto.logs_config.get("enabled"):
        account_id = get_aws_account_id()

        cw_policy_statements = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ],
                    "Resource": [f"arn:aws:logs:ap-south-1:{account_id}:*"],
                }
            ],
        }

        assume_role_policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Principal": {"Service": "appsync.amazonaws.com"},
                    "Action": "sts:AssumeRole",
                }
            ],
        }

        service_role_name = (
            f"{graphql_api_dto.api_name}-appsync-graphqlapi-logs"[:64]
        )

        response = create_service_role(
            role_name=service_role_name, policy_doc=assume_role_policy_doc
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Service role for {graphql_api_dto.api_name} CW Logs "
                }
            )
            return response

        inline_policy_name = (
            f"{graphql_api_dto.api_name}-appsync-graphqlapi-cw-logs-access"[
                :128
            ]
        )

        response = put_inline_policy_to_role(
            role_name=service_role_name,
            policy_name=inline_policy_name,
            policy_doc=cw_policy_statements,
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Inline Policy for Service Role of  {graphql_api_dto.api_name} CW Logs"
                }
            )
            return response

        cw_service_role_arn = (
            f"arn:aws:iam::{account_id}:role/service-role/{service_role_name}"
        )

        logs_config = {
            "fieldLogLevel": graphql_api_dto.logs_config.get(
                "fieldLogLevel", "ERROR"
            ),
            "cloudWatchLogsRoleArn": cw_service_role_arn,
            "excludeVerboseContent": graphql_api_dto.logs_config.get(
                "excludeVerboseContent", True
            ),
        }

        params.update({"logConfig": logs_config})

    try:
        response = app_sync_client.update_graphql_api(**params)

    except Exception as e:
        response = {"errors": str(e)}

    return response


def get_or_create_graphql_api(graphql_api_dto: GraphQLAPIDTO):
    # Create App Sync API
    # TODO Check whether logs are creating or not

    response = get_api_details(
        api_name=graphql_api_dto.api_name,
        authentication_type=graphql_api_dto.authentication_type,
    )

    if response and response.get("errors"):
        return response

    if response:
        api_details = response["graphqlApi"]
        print(
            f"Appsync API '{graphql_api_dto.api_name}' Already exists skipping creation"
        )

        if (
            api_details["authenticationType"]
            != graphql_api_dto.authentication_type
            or api_details.get("logConfig") != graphql_api_dto.logs_config
        ):

            print("Updating API...")

            response = update_authentication_type_of_graphql_api(
                api_id=api_details["apiId"], graphql_api_dto=graphql_api_dto
            )

            if response and response.get("errors"):
                return response
    else:
        response = create_graphql_api(graphql_api_dto)

        if response and response.get("errors"):
            return response

        api_details = response["graphqlApi"]

    if graphql_api_dto.authentication_type == AuthenticationType.API_KEY.value:

        print("Creating Appsync API")

        valid_api_keys = get_valid_api_keys_of_api(api_id=api_details["apiId"])

        if valid_api_keys:
            # DEBUG
            # print("Valid API Keys: ", len(valid_api_keys))

            api_key = valid_api_keys[0]["id"]
        else:
            response = create_api_key(
                api_id=api_details["apiId"],
                expires_in_seconds=graphql_api_dto.api_key_expires_in_seconds,
            )

            if response.get("errors"):
                return response

            api_key = response["apiKey"]["id"]

        api_details.update({"api_key": api_key})

    return api_details


def start_schema_creation(api_id: str, definition: bytes):
    # Add Schema to API
    try:
        response = app_sync_client.start_schema_creation(
            apiId=api_id, definition=definition
        )
    except Exception as e:
        # print(f"ERROR: {str(e)}")
        return {"errors": str(e)}

    return response


def get_schema_creation_status(api_id):
    try:
        response = app_sync_client.get_schema_creation_status(apiId=api_id)
    except Exception as e:
        return {"errors": str(e)}

    return response


def create_schema(api_id: str, definition: bytes):
    print("Creating/Updating Schema....")

    response = start_schema_creation(api_id=api_id, definition=definition)

    if response.get("errors"):
        return response

    while True:
        schema_creation_status = get_schema_creation_status(api_id=api_id)
        is_schema_creation_done = schema_creation_status["status"] == "SUCCESS"
        is_schema_creation_failed = (
            schema_creation_status["status"] == "FAILED"
        )

        if is_schema_creation_done:
            response["status"] = schema_creation_status
            return response

        if is_schema_creation_failed:
            response = {"errors": schema_creation_status}

            return response
        if schema_creation_status["status"] == "NOT_APPLICABLE":
            response = {"errors": schema_creation_status}
            return response


def create_service_role(role_name, policy_doc):
    try:
        response = iam_client.create_role(
            Path="/service-role/",
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(policy_doc),
        )
    except iam_client.exceptions.EntityAlreadyExistsException:
        response = iam_client.get_role(RoleName=role_name)
    except Exception as e:
        return {"errors": str(e)}

    return response["Role"]


def put_inline_policy_to_role(role_name, policy_name, policy_doc: Dict):
    try:
        response = iam_client.put_role_policy(
            RoleName=role_name,
            PolicyName=policy_name,
            PolicyDocument=json.dumps(policy_doc),
        )
    except Exception as e:
        response = {"errors": str(e)}

    return response


def get_data_source_details(name, api_id):
    try:
        response = app_sync_client.get_data_source(apiId=api_id, name=name)
    except Exception:
        return

    return response


def create_data_source(params):
    print(f"Creating Data Source {params['name']} ...")
    # DEBUG
    # print(f"Params {params}")

    try:
        response = app_sync_client.create_data_source(**params)
        # print("Data Source Creation Done")

    except Exception as e:
        return {"errors": str(e)}

    return response


def update_data_source(params):
    print(f"Updating Data Source {params['name']} ...")

    try:
        response = app_sync_client.update_data_source(**params)
        # print("Data Source Updated")

    except Exception as e:
        return {"errors": str(e)}

    return response


def create_or_update_data_source(
    data_source_dto: DataSourceDTO, api_name: str
):
    # Create Data Source(s)

    params = {
        "apiId": data_source_dto.api_id,
        "name": data_source_dto.name,
        "description": data_source_dto.description,
        "type": data_source_dto.data_source_type,
    }

    app_sync_assume_role_policy_doc = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Effect": "Allow",
                "Principal": {"Service": "appsync.amazonaws.com"},
                "Action": "sts:AssumeRole",
            }
        ],
    }

    if (
        data_source_dto.data_source_type
        == DataSourceType.AMAZON_DYNAMODB.value
    ):
        """
        Config: {
            'tableName': 'string',
            'awsRegion': 'string',
            'useCallerCredentials': True|False,
            'deltaSyncConfig': {
                'baseTableTTL': 123,
                'deltaSyncTableName': 'string',
                'deltaSyncTableTTL': 123
            },
            'versioned': True|False
        }
        """
        role_name = f"{api_name}-{data_source_dto.name}-appsync-role"[:64]

        response = create_service_role(
            role_name, app_sync_assume_role_policy_doc
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Service role for {data_source_dto.name}"
                }
            )
            return response

        dynamodb_table_name = data_source_dto.config["tableName"]
        dynamodb_region = data_source_dto.config["awsRegion"]

        account_id = get_aws_account_id()

        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "dynamodb:DeleteItem",
                        "dynamodb:GetItem",
                        "dynamodb:PutItem",
                        "dynamodb:Query",
                        "dynamodb:Scan",
                        "dynamodb:UpdateItem",
                    ],
                    "Resource": [
                        f"arn:aws:dynamodb:{dynamodb_region}:{account_id}:table/{dynamodb_table_name}",
                        f"arn:aws:dynamodb:{dynamodb_region}:{account_id}:table/{dynamodb_table_name}/*",
                    ],
                }
            ],
        }

        response = put_inline_policy_to_role(
            role_name=role_name,
            policy_name=f"{role_name}-inline-policy"[:128],
            policy_doc=policy_doc,
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Inline Policy for Service Role of {data_source_dto.name}"
                }
            )
            return response

        service_role_arn = (
            f"arn:aws:iam::{account_id}:role/service-role/{role_name}"
        )

        params.update({"serviceRoleArn": service_role_arn})

        params.update({"dynamodbConfig": data_source_dto.config})

    if (
        data_source_dto.data_source_type
        == DataSourceType.AMAZON_ELASTICSEARCH.value
    ):
        """
        elasticsearchConfig: {
            'endpoint': 'string',
            'awsRegion': 'string'
        }
        """
        role_name = f"{api_name}-{data_source_dto.name}-appsync-role"[:64]
        es_endpoint = data_source_dto.config["endpoint"]
        es_region = data_source_dto.config["region"]

        account_id = get_aws_account_id()

        response = create_service_role(
            role_name, app_sync_assume_role_policy_doc
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Service role for {data_source_dto.name}"
                }
            )
            return response

        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "es:ESHttpDelete",
                        "es:ESHttpHead",
                        "es:ESHttpGet",
                        "es:ESHttpPost",
                        "es:ESHttpPut",
                    ],
                    "Resource": [
                        f"arn:aws:es:{es_region}:{account_id}:domain/{es_endpoint}"
                    ],
                }
            ],
        }

        response = put_inline_policy_to_role(
            role_name=role_name,
            policy_name=f"{role_name}-inline-policy"[:128],
            policy_doc=policy_doc,
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Inline Policy for Service Role of {data_source_dto.name}"
                }
            )
            return response

        service_role_arn = (
            f"arn:aws:iam::{account_id}:role/service-role/{role_name}"
        )

        params.update({"serviceRoleArn": service_role_arn})

        params.update({"elasticsearchConfig": data_source_dto.config})

    if (
        data_source_dto.data_source_type
        == DataSourceType.AMAZON_OPENSEARCH_SERVICE.value
    ):
        """
        openSearchServiceConfig: {
            'endpoint': 'string',
            'awsRegion': 'string'
        }
        """

        role_name = f"{api_name}-{data_source_dto.name}-appsync-role"[:64]
        os_endpoint = data_source_dto.config["endpoint"]
        os_region = data_source_dto.config["awsRegion"]

        account_id = get_aws_account_id()

        response = create_service_role(
            role_name, app_sync_assume_role_policy_doc
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Service role for {data_source_dto.name}"
                }
            )
            return response

        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": [
                        "es:ESHttpDelete",
                        "es:ESHttpHead",
                        "es:ESHttpGet",
                        "es:ESHttpPost",
                        "es:ESHttpPut",
                    ],
                    "Resource": [
                        f"arn:aws:es:{os_region}:{account_id}:domain/{os_endpoint}"
                    ],
                }
            ],
        }

        response = put_inline_policy_to_role(
            role_name=role_name,
            policy_name=f"{role_name}-inline-policy"[:128],
            policy_doc=policy_doc,
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Inline Policy for Service Role of {data_source_dto.name}"
                }
            )
            return response

        service_role_arn = (
            f"arn:aws:iam::{account_id}:role/service-role/{role_name}"
        )

        params.update({"serviceRoleArn": service_role_arn})

        params.update({"openSearchServiceConfig": data_source_dto.config})

    if data_source_dto.data_source_type == DataSourceType.AWS_LAMBDA.value:
        """
        lambdaConfig: {
            'lambdaFunctionArn': 'string'
        }
        """
        role_name = f"{api_name}-{data_source_dto.name}-appsync-role"[:64]
        lambda_function_name = data_source_dto.config["lambdaFunctionName"]
        lambda_function_region = data_source_dto.config["region"]

        account_id = get_aws_account_id()

        response = create_service_role(
            role_name, app_sync_assume_role_policy_doc
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Service role for {data_source_dto.name}"
                }
            )
            return response

        policy_doc = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Effect": "Allow",
                    "Action": ["lambda:invokeFunction"],
                    "Resource": [
                        f"arn:aws:lambda:{lambda_function_region}:{account_id}:function:{lambda_function_name}",
                        f"arn:aws:lambda:{lambda_function_region}:{account_id}:function:{lambda_function_name}:*",
                    ],
                }
            ],
        }

        response = put_inline_policy_to_role(
            role_name=role_name,
            policy_name=f"{role_name}-inline-policy"[:128],
            policy_doc=policy_doc,
        )

        if response.get("errors"):
            response.update(
                {
                    "detail": f"Error while creating Inline Policy for Service Role of {data_source_dto.name}"
                }
            )
            return response

        service_role_arn = (
            f"arn:aws:iam::{account_id}:role/service-role/{role_name}"
        )

        params.update({"serviceRoleArn": service_role_arn})

        lambda_function_arn = f"arn:aws:lambda:{lambda_function_region}:{account_id}:function:{lambda_function_name}"
        params.update(
            {"lambdaConfig": {"lambdaFunctionArn": lambda_function_arn}}
        )

    if data_source_dto.data_source_type == DataSourceType.HTTP.value:
        # """
        # httpConfig: {
        #     'endpoint': 'string',
        #     'authorizationConfig': {
        #         'authorizationType': 'AWS_IAM',
        #         'awsIamConfig': {
        #             'signingRegion': 'string',
        #             'signingServiceName': 'string'
        #         }
        #     }
        # }
        # """
        # params.update({"httpConfig": data_source_dto.config})
        raise NotImplementedError()

    if (
        data_source_dto.data_source_type
        == DataSourceType.RELATIONAL_DATABASE.value
    ):
        # """
        # relationalDatabaseConfig: {
        #     'relationalDatabaseSourceType': 'RDS_HTTP_ENDPOINT',
        #     'rdsHttpEndpointConfig': {
        #         'awsRegion': 'string',
        #         'dbClusterIdentifier': 'string',
        #         'databaseName': 'string',
        #         'schema': 'string',
        #         'awsSecretStoreArn': 'string'
        #     }
        # }
        # """
        # params.update({"relationalDatabaseConfig": data_source_dto.config})
        # params.update(
        #     {
        #         "serviceRoleArn": "arn:aws:iam::995034872783:role/service-role/fb_posts-DDB_Source-appsync-role"
        #     }
        # )
        raise NotImplementedError()

    data_source_details = get_data_source_details(
        name=data_source_dto.name, api_id=data_source_dto.api_id
    )

    if data_source_details:
        response = update_data_source(params=params)

    else:
        response = create_data_source(params=params)

    return response


def get_function_details(name, api_id, data_source_name):
    nextToken = "init"

    while nextToken:
        if nextToken != "init":
            response = app_sync_client.list_functions(
                apiId=api_id, nextToken=nextToken, maxResults=25
            )
        else:
            response = app_sync_client.list_functions(
                apiId=api_id, maxResults=25
            )

        for function in response.get("functions", []):
            if (
                function["name"] == name
                and function["dataSourceName"] == data_source_name
            ):
                return function
        nextToken = response.get("nextToken")

    return


def create_function(function_dto: FunctionDTO):
    print(f"Creating Function {function_dto.name}")

    params = {
        "apiId": function_dto.api_id,
        "name": function_dto.name,
        "description": function_dto.description,
        "dataSourceName": function_dto.data_source_name,
        "functionVersion": function_dto.function_version,
    }

    if function_dto.sync_config:
        params.update({"syncConfig": function_dto.sync_config})

    if function_dto.request_mapping_template:
        params.update(
            {"requestMappingTemplate": function_dto.request_mapping_template}
        )

    if function_dto.response_mapping_template:
        params.update(
            {"responseMappingTemplate": function_dto.response_mapping_template}
        )

    try:
        response = app_sync_client.create_function(**params)
    except Exception as e:
        return {"errors": str(e)}

    return response


def update_function(function_dto: FunctionDTO):
    print(f"Updating Function {function_dto.name}")

    params = {
        "apiId": function_dto.api_id,
        "functionId": function_dto.function_id,
        "name": function_dto.name,
        "description": function_dto.description,
        "dataSourceName": function_dto.data_source_name,
        "functionVersion": function_dto.function_version,
    }

    if function_dto.sync_config:
        params.update({"syncConfig": function_dto.sync_config})

    if function_dto.request_mapping_template:
        params.update(
            {"requestMappingTemplate": function_dto.request_mapping_template}
        )

    if function_dto.response_mapping_template:
        params.update(
            {"responseMappingTemplate": function_dto.response_mapping_template}
        )

    try:
        response = app_sync_client.update_function(**params)
    except Exception as e:
        return {"errors": str(e)}

    return response


def create_or_update_function(function_dto: FunctionDTO):
    function_details = get_function_details(
        name=function_dto.name,
        api_id=function_dto.api_id,
        data_source_name=function_dto.data_source_name,
    )

    if function_details:
        function_dto = FunctionDTO(
            api_id=function_dto.api_id,
            function_id=function_details["functionId"],
            name=function_dto.name,
            description=function_dto.description,
            data_source_name=function_dto.data_source_name,
            request_mapping_template=function_dto.request_mapping_template,
            response_mapping_template=function_dto.response_mapping_template,
            function_version=function_dto.function_version,
            sync_config=function_dto.sync_config,
        )

        response = update_function(function_dto=function_dto)
    else:
        response = create_function(function_dto=function_dto)

    return response


def get_resolver_details(resolver_dto):
    try:
        response = app_sync_client.get_resolver(
            apiId=resolver_dto.api_id,
            typeName=resolver_dto.type_name,
            fieldName=resolver_dto.field_name,
        )
    except Exception as e:
        return {"errors": str(e)}

    return response


def update_resolver(params):
    try:
        response = app_sync_client.update_resolver(**params)
    except Exception as e:
        return {"errors": str(e)}
    return response


def create_resolver(params):
    try:
        response = app_sync_client.create_resolver(**params)
    except Exception as e:
        return {"errors": str(e)}

    return response


def create_or_update_resolver(resolver_dto: ResolverDTO, region):
    params = {
        "apiId": resolver_dto.api_id,
        "typeName": resolver_dto.type_name,
        "fieldName": resolver_dto.field_name,
        "dataSourceName": resolver_dto.data_source_name,
        "kind": resolver_dto.kind,
    }

    if resolver_dto.request_mapping_template:
        params.update(
            {"requestMappingTemplate": resolver_dto.request_mapping_template}
        )

    if resolver_dto.response_mapping_template:
        params.update(
            {"responseMappingTemplate": resolver_dto.response_mapping_template}
        )

    if resolver_dto.pipeline_config:
        params.pop("dataSourceName")

        function_ids = []

        for function in resolver_dto.pipeline_config["functions"]:
            function_id = get_function_details(
                name=function["name"],
                api_id=resolver_dto.api_id,
                data_source_name=function["dataSourceName"],
            )["functionId"]

            if not function_id:
                return {
                    "errors": f"Function with name {function['name']} and data src: {function['dataSourceName']} Doesn't Exist "
                }

            function_ids.append(function_id)

        params.update({"pipelineConfig": {"functions": function_ids}})

    if resolver_dto.caching_config:
        params.update({"cachingConfig": resolver_dto.caching_config})

    if resolver_dto.sync_config:
        sync_config = resolver_dto.sync_config

        if sync_config.get("lambdaConflictHandlerConfig"):
            if sync_config["lambdaConflictHandlerConfig"].get(
                "lambdaFunctionName"
            ):
                func_name = sync_config["lambdaConflictHandlerConfig"].get(
                    "lambdaFunctionName"
                )
                lambda_function_arn = get_lambda_func_arn(
                    func_name=func_name, region=region
                )
                sync_config["lambdaConflictHandlerConfig"][
                    "lambdaConflictHandlerArn"
                ] = lambda_function_arn
                sync_config["lambdaConflictHandlerConfig"].pop(
                    "lambdaFunctionName"
                )

        params.update({"syncConfig": sync_config})

    response = get_resolver_details(resolver_dto=resolver_dto)

    if response.get("errors"):
        response.update(
            {
                "details": f"Error While getting resolver details {resolver_dto.type_name}  > {resolver_dto.field_name}"
            }
        )
        if " No resolver found" not in response["errors"]:
            return response

    if response.get("resolver"):
        print(
            f"Updating Resolver {resolver_dto.type_name} > {resolver_dto.field_name} > {resolver_dto.data_source_name if not resolver_dto.pipeline_config else [' > '.join(func['name'] for func in resolver_dto.pipeline_config['functions'])]}"
        )

        response = update_resolver(params)

        if response.get("errors"):
            response.update(
                {
                    "details": f"Error While Updating resolver details {resolver_dto.type_name}  > {resolver_dto.field_name}"
                }
            )
            return response
    else:
        print(
            f"Creating Resolver {resolver_dto.type_name} > {resolver_dto.field_name} > {resolver_dto.data_source_name if not resolver_dto.pipeline_config else [' > '.join(func['name'] for func in resolver_dto.pipeline_config['functions'])]}"
        )

        response = create_resolver(params)
        if response.get("errors"):
            response.update(
                {
                    "details": f"Error While Creating resolver details {resolver_dto.type_name}  > {resolver_dto.field_name}"
                }
            )
            return response

    return response


def get_schema_types_of_api(api_id):
    nextToken = "init"

    schema_types = []

    while nextToken:
        if nextToken != "init":
            response = app_sync_client.list_types(
                apiId=api_id, format="JSON", nextToken=nextToken, maxResults=25
            )
        else:
            response = app_sync_client.list_types(
                apiId=api_id, format="JSON", maxResults=25
            )

        schema_types.extend(response["types"])

        nextToken = response.get("nextToken")

    return schema_types


def get_or_create_appsync_domain(domain, certificate_arn):
    try:
        response = app_sync_client.get_domain_name(domainName=domain)
    except app_sync_client.exceptions.NotFoundException:

        response = app_sync_client.create_domain_name(
            domainName=domain,
            certificateArn=certificate_arn,
            description="App Sync Domain",
        )
    except Exception as e:
        return {"errors": str(e)}

    return response


def get_api_association(domain):
    try:
        response = app_sync_client.get_api_association(domainName=domain)
    except app_sync_client.exceptions.NotFoundException as e:
        if "Domain name is not associated" in str(e):
            return
        else:
            return {"errors": str(e)}

    return response["apiAssociation"]


def get_domain_name(domain):
    try:
        response = app_sync_client.get_domain_name(domainName=domain)
    except Exception as e:
        return {"errors": str(e)}

    return response["domainNameConfig"]


def associate_api_with_custom_domain(api_id, domain, certificate_arn):
    print(f"Associating API With Custom Domain {domain}")

    response = get_or_create_appsync_domain(
        domain, certificate_arn=certificate_arn
    )

    if response.get("errors"):
        return response

    associated_api = get_api_association(domain=domain)

    if (
        associated_api
        and associated_api.get("apiId")
        and api_id != associated_api["apiId"]
    ):
        return {
            "errors": f"Domain {domain} Associated with another api (apiId: {associated_api['apiId']}) currently"
        }

    try:
        response = app_sync_client.associate_api(
            domainName=domain, apiId=api_id
        )
    except Exception as e:
        return {"errors": str(e)}

    while True:
        associated_api = get_api_association(domain)

        association_status = associated_api["associationStatus"]

        if association_status == "PROCESSING":
            sleep(2)
            continue

        if association_status == "SUCCESS":
            print("API Associated with Domain Successfully")
            break
        elif association_status == "FAILED":
            return {
                "errors": "Association Failed",
                "details": associated_api.get("deploymentDetail"),
            }

    response = create_r53_record_for_api(domain=domain)

    return response


def get_best_match_zone(domain):
    """Return zone id which name is closer matched with domain name."""

    host_zones = []

    nextMarker = "init"

    while nextMarker:
        if nextMarker != "init":
            response = r_53_client.list_hosted_zones(
                Marker=nextMarker, MaxItems=25
            )
        else:
            response = r_53_client.list_hosted_zones(MaxItems="25")

        host_zones.extend(response["HostedZones"])

        nextMarker = response.get("NextMarker")

    public_zones = [
        zone for zone in host_zones if not zone["Config"]["PrivateZone"]
    ]

    """
    Suppose there are two hosted zones `api.in` and `beta.api.in` and domain name specified is `some-beta.api.in`
    The previous logic selects hosted `beta.api.in` as the hosted zone for the specified domain.
    The new logic will return `api.in` after checking whether exact match of domain exists or not.
    """

    zones = {
        zone["Name"][:-1]: zone
        for zone in public_zones
        if zone["Name"][:-1] == domain
    }

    if not zones:
        zones = {
            zone["Name"][:-1]: zone
            for zone in public_zones
            if "." + zone["Name"][:-1] in domain
        }

    if zones:
        keys = max(
            zones.keys(), key=lambda a: len(a)
        )  # get longest key -- best match.
        return zones[keys]
    else:
        return None


def create_r53_record_for_api(domain):
    domain_hosted_zone = get_best_match_zone(domain=domain)

    print(f"Domain Host Zone: {domain_hosted_zone}")

    if not domain_hosted_zone:
        return {"errors": f"Hosted Zone not found for domain {domain}"}

    domain_hosted_zone_id = domain_hosted_zone["Id"]

    print("Domain Host Id: ", domain_hosted_zone_id)

    response = get_domain_name(domain=domain)

    if response.get("errors"):
        return response

    app_sync_domain_name = response["appsyncDomainName"].rstrip(".")
    # DEBUG
    # print(f"App Sync domain : {app_sync_domain_name}")

    response["hostedZoneId"]

    # DEBUG
    # print(f"App sync Host Zone id: {app_sync_host_zone_id}")

    if not domain_hosted_zone_id:
        return {"errors": f"Unable to find Hostzone for domain {domain}"}

    try:
        response = r_53_client.change_resource_record_sets(
            HostedZoneId=domain_hosted_zone_id,
            ChangeBatch={
                "Comment": "",
                "Changes": [
                    {
                        "Action": "UPSERT",
                        "ResourceRecordSet": {
                            "Type": "CNAME",
                            "Name": domain,
                            "ResourceRecords": [
                                {"Value": app_sync_domain_name}
                            ],
                            "TTL": 300,
                        },
                    }
                ],
            },
        )
    except Exception as e:
        return {"errors": str(e)}

    return response


def main(stage: str):
    def setup_appsync(graphql_config_path: str):
        config_path = os.path.join(
            graphql_config_path, "appsync_settings.json"
        )
        app_sync_config_file = open(config_path, "r")
        app_sync_config = json.load(app_sync_config_file)
        app_sync_config_stage = app_sync_config[stage]
        app_sync_config_file.close()
        api_name = app_sync_config_stage["apiName"]
        domain = app_sync_config_stage.get("domain")
        certificate_arn = app_sync_config_stage.get("certificate_arn")
        region = app_sync_config_stage["region"]
        logs_config = app_sync_config_stage["logs_config"]
        cache_config = app_sync_config_stage.get("cache_config", {})
        authentication_type = app_sync_config_stage["authenticationType"]
        lambda_authorizer_config = app_sync_config_stage.get(
            "lambdaAuthorizerConfig", {}
        )
        open_id_connect_config = app_sync_config_stage.get(
            "openIDConnectConfig", {}
        )
        user_pool_config = app_sync_config_stage.get("userPoolConfig", {})
        data_sources = app_sync_config_stage["dataSources"]
        functions = app_sync_config["functions"]
        resolvers = app_sync_config["resolvers"]
        default_resolver = app_sync_config["resolvers"]["DEFAULT_RESOLVER"]
        resolvers.pop("DEFAULT_RESOLVER")

        subscriptions = app_sync_config["resolvers"][
            "DEFAULT_RESOLVER_SUBSCRIPTIONS"
        ]
        resolvers.pop("DEFAULT_RESOLVER_SUBSCRIPTIONS")

        subscriptions_default_resolver = app_sync_config["resolvers"][
            "DEFAULT_SUBSCRIPTION_RESOLVER"
        ]
        resolvers.pop("DEFAULT_SUBSCRIPTION_RESOLVER")

        if authentication_type == "AWS_LAMBDA" and lambda_authorizer_config:
            lambda_authorizer_config = {
                "authorizerResultTtlInSeconds": lambda_authorizer_config.get(
                    "authorizerResultTtlInSeconds", 0
                ),
                "authorizerUri": get_lambda_func_arn(
                    func_name=lambda_authorizer_config["lambdaFunctionName"],
                    region=lambda_authorizer_config.get("region", region),
                ),
                "identityValidationExpression": lambda_authorizer_config.get(
                    "identityValidationExpression", ""
                ),
            }

        graphql_api_dto = GraphQLAPIDTO(
            api_name=api_name,
            region=region,
            authentication_type=authentication_type,
            user_pool_config=user_pool_config,
            open_id_connect_config=open_id_connect_config,
            lambda_authorizer_config=lambda_authorizer_config,
            logs_config=logs_config,
        )

        # Create API
        response = get_or_create_graphql_api(graphql_api_dto=graphql_api_dto)

        if response.get("errors"):
            print(f"ERROR: {response['errors']}")
            raise Exception()

        api_id = response["apiId"]

        # Custom Domain
        if domain:
            response = associate_api_with_custom_domain(
                api_id=api_id, domain=domain, certificate_arn=certificate_arn
            )

        if response.get("errors"):
            print(f"ERROR: {response['errors']}")
            raise Exception()

        # Create Schema

        # TODO Update this path
        # Cache Config
        if cache_config.get("enabled"):
            cache_dto = CacheDTO(
                api_id=api_id,
                ttl=cache_config.get("ttl", 3600),
                apiCachingBehavior=cache_config["apiCachingBehavior"],
                type=cache_config["type"],
                transitEncryptionEnabled=cache_config[
                    "transitEncryptionEnabled"
                ],
                atRestEncryptionEnabled=cache_config[
                    "atRestEncryptionEnabled"
                ],
            )

            create_api_cache(cache_dto=cache_dto)

        schema_file_path = os.path.join(graphql_config_path, "schema.graphql")

        with open(schema_file_path, mode="r") as schema_file:
            schema_definition = bytes(schema_file.read(), "utf-8")

        response = create_schema(api_id=api_id, definition=schema_definition)

        if response.get("errors"):
            print(f"ERROR: {response['errors']}")
            raise Exception()

        # Create Data Sources

        for data_source in data_sources:
            data_source_dto = DataSourceDTO(
                api_id=api_id,
                name=data_source["name"],
                description=data_source.get("description"),
                data_source_type=data_source["type"],
                config=data_source.get("config"),
            )

            response = create_or_update_data_source(
                data_source_dto=data_source_dto, api_name=api_name
            )

            if response.get("errors"):
                print(f"ERROR: {response}")
                return
            # print(f"Data Source, {data_source_dto.name} Created Successfully")

        for function in functions:
            request_mapping_template_file_path = function.get(
                "requestMappingTemplate"
            )

            with open(
                request_mapping_template_file_path, mode="r"
            ) as request_mapping_template_file:
                request_mapping_template = request_mapping_template_file.read()

            response_mapping_template_file_path = function.get(
                "responseMappingTemplate"
            )

            with open(
                response_mapping_template_file_path, mode="r"
            ) as response_mapping_template_file:
                response_mapping_template = (
                    response_mapping_template_file.read()
                )

            function_dto = FunctionDTO(
                api_id=api_id,
                name=function["name"],
                description=function.get("description", ""),
                data_source_name=function["dataSourceName"],
                request_mapping_template=request_mapping_template,
                response_mapping_template=response_mapping_template,
                sync_config=function.get("syncConfig"),
            )

            response = create_or_update_function(function_dto=function_dto)

            if response.get("errors"):
                print(f"ERROR: {response['errors']}")
                raise Exception()

        schema_types = get_schema_types_of_api(api_id=api_id)

        # Resolvers can be attached only for OBJECTS

        valid_schema_types = [
            schema_type
            for schema_type in schema_types
            if json.loads(schema_type["definition"])["kind"] == "OBJECT"
        ]

        for schema_type in valid_schema_types:
            definition = json.loads(schema_type["definition"])

            if definition["name"] not in ["Query", "Mutation", "Subscription"]:
                continue

            fields = [field["name"] for field in definition["fields"]]

            for field in fields:
                if resolvers.get(schema_type["name"]) and resolvers[
                    schema_type["name"]
                ].get(field):
                    resolver_config = resolvers[schema_type["name"]][field]
                elif schema_type["name"] != "Subscription":
                    resolver_config = default_resolver
                elif field in subscriptions:
                    resolver_config = subscriptions_default_resolver
                else:
                    continue

                request_mapping_template_file_path = resolver_config.get(
                    "requestMappingTemplate"
                )

                with open(
                    request_mapping_template_file_path, mode="r"
                ) as request_mapping_template_file:
                    request_mapping_template = (
                        request_mapping_template_file.read()
                    )

                response_mapping_template_file_path = resolver_config.get(
                    "responseMappingTemplate"
                )

                with open(
                    response_mapping_template_file_path, mode="r"
                ) as response_mapping_template_file:
                    response_mapping_template = (
                        response_mapping_template_file.read()
                    )

                resolver_dto = ResolverDTO(
                    api_id=api_id,
                    type_name=schema_type["name"],
                    field_name=field,
                    data_source_name=resolver_config.get("dataSourceName"),
                    kind=resolver_config.get("kind", "UNIT"),
                    request_mapping_template=request_mapping_template,
                    response_mapping_template=response_mapping_template,
                    pipeline_config=resolver_config.get("pipelineConfig"),
                    sync_config=resolver_config.get("syncConfig"),
                    caching_config=resolver_config.get("cachingConfig"),
                )

                response = create_or_update_resolver(
                    resolver_dto=resolver_dto, region=region
                )

                if response.get("errors"):
                    print(f"ERROR: {response['errors']}")
                    raise Exception()

        print("Setup Done")

    # apps = settings.INSTALLED_APPS
    # DEBUG
    # print("Apps", apps)
    base_path = os.getcwd()

    # for app in apps:
    #     graphql_config_path = os.path.join(base_path, app, "graphql")
    #     app_sync_config_path = os.path.join(graphql_config_path, "app_sync_config.json")
    #
    #     is_app_sync_config_exists = os.path.exists(app_sync_config_path)
    #
    #     if not is_app_sync_config_exists:
    #         # DEBUG
    #         # print(f"{app}: Path Doesn't Exists")
    #         continue
    #
    # print(f"Setting up for {app}...")

    config_path = os.path.join(base_path, "graphql_service")

    setup_appsync(graphql_config_path=config_path)


if __name__ == "__main__":
    # parser = argparse.ArgumentParser()
    # parser.add_argument("-s", "--stage", help="Stage")
    # args = parser.parse_args()
    #
    # if args.stage:
    # stage = args.stage

    import sys

    args = sys.argv

    main(stage=args[1])
