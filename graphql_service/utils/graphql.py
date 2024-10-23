
from typing import Optional, Sequence

from graphql import GraphQLError, parse

from graphql_service.utils.logger import log_error


def handle_query_result(
    result, *, logger, error_formatter, debug, extension_manager=None
):
    response = {"data": result.data}
    if result.errors:
        for error in result.errors:
            log_error(error, logger)
        response["errors"] = [
            error_formatter(error, debug) for error in result.errors
        ]

    return True, response


def handle_graphql_errors(
    errors: Sequence[GraphQLError],
    *,
    logger,
    error_formatter,
    debug,
):
    for error in errors:
        log_error(error, logger)
    response = {"errors": [error_formatter(error, debug) for error in errors]}
    return False, response


def parse_query(query):
    try:
        return parse(query)
    except GraphQLError as error:
        raise error
    except Exception as error:
        raise GraphQLError(str(error)) from error


def validate_data(data: Optional[dict]) -> None:
    if not isinstance(data, dict):
        raise GraphQLError("Operation data should be a JSON object")
    validate_query_body(data.get("query"))
    validate_variables(data.get("variables"))
    validate_operation_name(data.get("operationName"))


def validate_query_body(query) -> None:
    if not query or not isinstance(query, str):
        raise GraphQLError("The query must be a string.")


def validate_variables(variables) -> None:
    if variables is not None and not isinstance(variables, dict):
        raise GraphQLError("Query variables must be a null or an object.")


def validate_operation_name(operation_name) -> None:
    if operation_name is not None and not isinstance(operation_name, str):
        raise GraphQLError(
            '"%s" is not a valid operation name.' % operation_name
        )
