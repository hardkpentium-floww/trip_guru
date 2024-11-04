
from reprlib import repr  # pylint: disable=redefined-builtin
from traceback import format_exception
from typing import List, Optional, cast

from django.conf import settings
from graphql.error import GraphQLError
from graphql.error.graphql_error import format_error as format_graphql_error

from graphql_service.utils import get_logger
from graphql_service.utils.utils import unwrap_graphql_error

unhandled_errors_logger = get_logger(__name__)


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
    if settings.DEBUG:
        lines = []
        if isinstance(exc, BaseException):
            for line in traceback.format_exception(
                type(exc), exc, exc.__traceback__
            ):
                lines.extend(line.rstrip().splitlines())
        result["extensions"]["exception"]["stacktrace"] = lines
    return result


def get_error_extension(error: GraphQLError) -> Optional[dict]:
    unwrapped_error = unwrap_graphql_error(error)
    if unwrapped_error is None or not error.__traceback__:
        return None

    unwrapped_error = cast(Exception, unwrapped_error)
    return {
        "stacktrace": get_formatted_error_traceback(unwrapped_error),
        "context": get_formatted_error_context(unwrapped_error),
    }


def get_formatted_error_traceback(error: Exception) -> List[str]:
    formatted = []
    for line in format_exception(type(error), error, error.__traceback__):
        formatted.extend(line.rstrip().splitlines())
    return formatted


def get_formatted_error_context(error: Exception) -> Optional[dict]:
    tb_last = error.__traceback__
    while tb_last and tb_last.tb_next:
        tb_last = tb_last.tb_next
    if tb_last is None:
        return None
    return {
        key: repr(value) for key, value in tb_last.tb_frame.f_locals.items()
    }
