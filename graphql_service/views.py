import importlib
import inspect
import json
import re
import time
from typing import Sequence

import graphene
from django.http import HttpResponse, HttpResponseNotAllowed
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from graphql.error import GraphQLError
from graphql.error.graphql_error import format_error as format_graphql_error
from graphql.execution import ExecutionResult
from graphql.execution.middleware import MiddlewareManager
from rest_framework import exceptions, permissions, status
from rest_framework.views import APIView
from structlog.contextvars import (
    bind_contextvars,
    clear_contextvars,
    get_merged_contextvars,
)

from graphql_service.utils import get_logger
from graphql_service.utils.logger import log_error

unhandled_errors_logger = get_logger(__name__)


class HttpError(Exception):
    def __init__(self, response, message=None, *args, **kwargs):
        self.response = response
        self.message = message = message or response.content.decode()
        super(HttpError, self).__init__(message, *args, **kwargs)


def get_accepted_content_types(request):
    def qualify(x):
        parts = x.split(";", 1)
        if len(parts) == 2:
            match = re.match(
                r"(^|;)q=(0(\.\d{,3})?|1(\.0{,3})?)(;|$)", parts[1]
            )
            if match:
                return parts[0].strip(), float(match.group(2))
        return parts[0].strip(), 1

    raw_content_types = request.META.get("HTTP_ACCEPT", "*/*").split(",")
    qualified_content_types = map(qualify, raw_content_types)
    return list(
        x[0]
        for x in sorted(
            qualified_content_types, key=lambda x: x[1], reverse=True
        )
    )


def instantiate_middleware(middlewares):
    for middleware in middlewares:
        if inspect.isclass(middleware):
            yield middleware()
            continue
        yield middleware


class GraphQLView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    schema = None
    middleware = None
    root_value = None
    pretty = False
    batch = False
    subscription_path = None
    execution_context_class = None
    headers = None

    def __init__(
        self,
        middleware=None,
        root_value=None,
        pretty=False,
        batch=False,
        execution_context_class=None,
        *args,
        **kwargs,
    ):
        if middleware is not None:
            if isinstance(middleware, MiddlewareManager):
                self.middleware = middleware
            else:
                self.middleware = list(instantiate_middleware(middleware))
        self.root_value = root_value
        self.pretty = self.pretty or pretty
        self.batch = self.batch or batch
        self.execution_context_class = execution_context_class

    # noinspection PyUnusedLocal
    def get_root_value(self, request):
        return self.root_value

    def get_middleware(self, request):
        return self.middleware

    @method_decorator(ensure_csrf_cookie)
    def dispatch(self, request, *args, **kwargs):
        log = configure_structlog()
        start_time = time.time()
        bind_contextvars(queryStartTime=start_time)
        bind_contextvars(funcsExecutionTime={})
        bind_contextvars(funcsReachAndExecutionTime={})
        request = self.initialize_request(request, *args, **kwargs)
        bind_contextvars(
            queryInitializationTime=(time.time() - start_time) * 1000
        )
        try:
            self.initial(request, *args, **kwargs)
            bind_contextvars(
                queryInitialTime=(time.time() - start_time) * 1000
            )

            request.user_id = str(request.user.user_id)
            request.exec_time = 0
            if request.method.lower() != "post":
                raise HttpError(
                    HttpResponseNotAllowed(
                        ["POST"],
                        "GraphQL only supports POST requests.",
                    )
                )

            data = request.data

            if self.batch:
                responses = [
                    self.get_response(request, entry) for entry in data
                ]
                result = "[{}]".format(
                    ",".join([response[0] for response in responses])
                )
                status_code = (
                    responses
                    and max(responses, key=lambda response: response[1])[1]
                    or 200
                )
            else:
                result, status_code = self.get_response(request, data)

            response = HttpResponse(
                status=status_code,
                content=result,
                content_type="application/json",
            )
            bind_contextvars(
                queryExecutionTime=(time.time() - start_time) * 1000
            )

            print(get_merged_contextvars(log))

            clear_contextvars()

            return response

        except Exception as e:
            print(get_merged_contextvars(log))

            clear_contextvars()
            return self.handle_exception(e)

    def handle_exception(self, exc):
        """
        Handle any exception that occurs, by returning an appropriate response,
        or re-raising the error.
        """
        if isinstance(
            exc, (exceptions.NotAuthenticated, exceptions.AuthenticationFailed)
        ):
            data = {
                "errors": [
                    {
                        "errorType": "UnauthorizedException",
                        "message": "You are not authorized to make this call.",
                    }
                ]
            }
            status_code = status.HTTP_401_UNAUTHORIZED
        else:
            error_class_name = str(type(exc))
            data = {
                "errors": [
                    {
                        "errorType": "BadRequestException",
                        "message": f"Your request is not valid, Please check: {error_class_name}",
                    }
                ]
            }
            status_code = status.HTTP_400_BAD_REQUEST

        return HttpResponse(
            status=status_code,
            content=json.dumps(data),
            content_type="application/json",
        )

    def get_response(self, request, data, show_graphiql=False):
        query, variables, operation_name, id = self.get_graphql_params(
            request, data
        )

        query_summery = {
            "queryName": operation_name,
            # "queryString": query,
            "variables": variables,
            "logType": "GRAPHENE_TRACING",
        }
        bind_contextvars(**query_summery)

        execution_result = self.execute_graphql_request(
            request, data, query, variables, operation_name, show_graphiql
        )

        status_code = 200
        if execution_result:
            response = {}

            if execution_result.errors:
                response["errors"] = [
                    self.format_error(e) for e in execution_result.errors
                ]
                self.handle_graphql_errors(
                    execution_result.errors, operation_name
                )

            if execution_result.errors and any(
                not getattr(e, "path", None) for e in execution_result.errors
            ):
                status_code = 400
            else:
                response["data"] = execution_result.data

            if self.batch:
                response["id"] = id
                response["status"] = status_code

            result = self.json_encode(request, response, pretty=show_graphiql)
        else:
            result = None

        return result, status_code

    @staticmethod
    def handle_graphql_errors(errors: Sequence[GraphQLError], operation_name):
        if errors is None:
            return
        try:
            for error in errors:
                _ = log_error(error=error, logger_name=operation_name)
        except Exception:
            pass

    def render_graphiql(self, request, **data):
        return render(request, self.graphiql_template, data)

    def json_encode(self, request, d, pretty=False):
        if not (self.pretty or pretty) and not request.GET.get("pretty"):
            return json.dumps(d, separators=(",", ":"))

        return json.dumps(d, sort_keys=True, indent=2, separators=(",", ": "))

    def parse_body(self, request):
        content_type = self.get_content_type(request)

        if content_type == "application/graphql":
            return {"query": request.body.decode()}

        elif content_type == "application/json":
            # noinspection PyBroadException
            try:
                body = request.body.decode("utf-8")
            except Exception as e:
                raise HttpError(HttpResponseBadRequest(str(e)))

            try:
                request_json = json.loads(body)
                if self.batch:
                    assert isinstance(request_json, list), (
                        "Batch requests should receive a list, but received {}."
                    ).format(repr(request_json))
                    assert (
                        len(request_json) > 0
                    ), "Received an empty list in the batch request."
                else:
                    assert isinstance(
                        request_json, dict
                    ), "The received data is not a valid JSON query."
                return request_json
            except AssertionError as e:
                raise HttpError(HttpResponseBadRequest(str(e)))
            except (TypeError, ValueError):
                raise HttpError(
                    HttpResponseBadRequest("POST body sent invalid JSON.")
                )

        elif content_type in [
            "application/x-www-form-urlencoded",
            "multipart/form-data",
        ]:
            return request.POST

        return {}

    def execute_graphql_request(
        self,
        request,
        data,
        query,
        variables,
        operation_name,
        show_graphiql=False,
    ):
        if not query:
            if show_graphiql:
                return None
            raise HttpError(
                HttpResponseBadRequest("Must provide query string.")
            )

        try:
            extra_options = {}
            if self.execution_context_class:
                extra_options[
                    "execution_context_class"
                ] = self.execution_context_class

            options = {
                "source": query,
                "root_value": self.get_root_value(request),
                "variable_values": variables,
                "operation_name": operation_name,
                "context_value": request,
                "middleware": self.get_middleware(request),
            }
            options.update(extra_options)

            return self.execute_graphql_as_sync(**options)
        except Exception as e:
            return ExecutionResult(errors=[e])

    def execute_graphql_as_sync(self, **options):
        from django.conf import settings

        if settings.SHOULD_USE_DYNAMIC_SCHEMA:
            start_time = time.time()

            schema = self.get_schema(query_string=options.get("source"))

            end_time = time.time() - start_time
            bind_contextvars(dynamicSchemaTime=end_time * 1000)
        else:
            start_time = time.time()

            end_time = time.time() - start_time
            bind_contextvars(dynamicSchemaTime=end_time * 1000)

        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(schema.execute_async(**options))
        loop.close()
        return result

    @classmethod
    def can_display_graphiql(cls, request, data):
        raw = "raw" in request.GET or "raw" in data
        return not raw and cls.request_wants_html(request)

    @classmethod
    def request_wants_html(cls, request):
        accepted = get_accepted_content_types(request)
        accepted_length = len(accepted)
        # the list will be ordered in preferred first - so we have to make
        # sure the most preferred gets the highest number
        html_priority = (
            accepted_length - accepted.index("text/html")
            if "text/html" in accepted
            else 0
        )
        json_priority = (
            accepted_length - accepted.index("application/json")
            if "application/json" in accepted
            else 0
        )

        return html_priority > json_priority

    @staticmethod
    def get_graphql_params(request, data):
        query = request.GET.get("query") or data.get("query")
        variables = request.GET.get("variables") or data.get("variables")
        id = request.GET.get("id") or data.get("id")

        if variables and isinstance(variables, str):
            try:
                variables = json.loads(variables)
            except Exception:
                raise HttpError(
                    HttpResponseBadRequest("Variables are invalid JSON.")
                )

        operation_name = request.GET.get("operationName") or data.get(
            "operationName"
        )
        if operation_name == "null":
            operation_name = None

        return query, variables, operation_name, id

    @staticmethod
    def format_error(error):
        import traceback

        if isinstance(error, GraphQLError):
            result = format_graphql_error(error)
        else:
            result = {"message": str(error)}

        if "extensions" not in result:
            result["extensions"] = {}

        exc = error
        while isinstance(exc, GraphQLError) and hasattr(exc, "original_error"):
            exc = exc.original_error
        if isinstance(exc, AssertionError):
            exc = GraphQLError(str(exc))

        result["extensions"]["exception"] = {"code": type(exc).__name__}

        from django.conf import settings

        if settings.DEBUG:
            lines = []
            if isinstance(exc, BaseException):
                for line in traceback.format_exception(
                    type(exc), exc, exc.__traceback__
                ):
                    lines.extend(line.rstrip().splitlines())
            result["extensions"]["exception"]["stacktrace"] = lines
        return result

    @staticmethod
    def get_content_type(request):
        meta = request.META
        content_type = meta.get(
            "CONTENT_TYPE", meta.get("HTTP_CONTENT_TYPE", "")
        )
        return content_type.split(";", 1)[0].lower()

    @staticmethod
    def get_schema(query_string):
        start_time = time.time()

        from graphql import parse

        document_node = parse(query_string)

        operation_names = [
            selection.name.value
            for selection in document_node.definitions[
                0
            ].selection_set.selections
        ]

        if "__typename" in operation_names:
            operation_names.remove("__typename")

        end_time = time.time() - start_time
        bind_contextvars(parsingTime=end_time * 1000)

        from graphql_service.schema_path_map import MUTATIONS, QUERIES

        query, mutation = None, None
        query_classes, mutation_classes = [], []

        for op_name in operation_names:
            if QUERIES.get(op_name):
                for query_class_path in QUERIES[op_name]:
                    module_path, class_import = query_class_path.rsplit(".", 1)
                    query_class = importlib.import_module(
                        module_path
                    ).__getattribute__(class_import)
                    query_classes.append(query_class)
            elif MUTATIONS.get(op_name):
                for mutation_class_path in MUTATIONS[op_name]:
                    module_path, class_import = mutation_class_path.rsplit(
                        ".", 1
                    )
                    mutation_class = importlib.import_module(
                        module_path
                    ).__getattribute__(class_import)
                    mutation_classes.append(mutation_class)
            else:
                raise Exception("Operation Not Registered In Dynamic Schema")

        # Since Query and mutation classes need to inherit
        # graphene.ObjectType and order must be last if used from importlib
        if query_classes:
            query_classes.append(graphene.ObjectType)
        if mutation_classes:
            mutation_classes.append(graphene.ObjectType)

        if query_classes:

            class Query(*query_classes):
                """
                Class to define the Query Object
                """

            query = Query

        if mutation_classes:

            class Mutation(*mutation_classes):
                """
                Class to define the Mutation Object
                """

            mutation = Mutation

        return graphene.Schema(query=query, mutation=mutation)


def print_tracing(_, __, event_dict):
    import json

    try:
        event_dict = json.loads(event_dict)
    except json.JSONDecodeError:
        pass

    print(event_dict)
    return {}


def configure_structlog():
    import structlog
    from structlog import configure
    from structlog.contextvars import merge_contextvars

    configure(
        processors=[
            merge_contextvars,
            structlog.processors.KeyValueRenderer(key_order=["event", "a"]),
            print_tracing,
        ]
    )
    log = structlog.get_logger()
    return log
