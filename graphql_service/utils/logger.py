
import logging
from typing import Optional

from graphql_service.utils.utils import unwrap_graphql_error


def log_error(error: Exception, logger_name: Optional[str] = None):
    original_error = unwrap_graphql_error(error)
    if original_error and original_error is not error:
        error.__suppress_context__ = True
        error.__cause__ = original_error

    logger = logging.getLogger(logger_name)
    logger.error(original_error, exc_info=original_error)
    return original_error
