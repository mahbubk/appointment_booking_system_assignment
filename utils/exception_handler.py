"""
Custom exception handler for Django REST Framework.

Handles known exceptions, logs them,
and returns a standardized error response format.
"""
import logging
import sys

from django.core.exceptions import ObjectDoesNotExist, ValidationError
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from utils.responses import Responses

logger = logging.getLogger("request_logger")

EXCEPTION_STATUS_MAPPING = {
    ValueError: status.HTTP_400_BAD_REQUEST,
    ObjectDoesNotExist: status.HTTP_400_BAD_REQUEST,
    ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
    APIException: status.HTTP_400_BAD_REQUEST,
    Exception: status.HTTP_500_INTERNAL_SERVER_ERROR,
}


def extract_error_message(exception):
    """Extract the error message from the exception."""
    if isinstance(exception, APIException):
        return exception.detail
    if hasattr(exception, "message"):
        return exception.message
    return str(exception)


def handle_exception(exception):
    """Handle the exception and return an appropriate Response."""
    error_message = extract_error_message(exception)

    if isinstance(error_message, dict) and "detail" in error_message:
        error_message = error_message["detail"]
    if isinstance(error_message, list):
        error_message = error_message[0] if error_message else "An error occurred"

    exc_info = sys.exc_info()
    logger.error("Exception caught: %s", error_message)
    logger.error(
        "Exception caught: %s", error_message, extra={"exc_info_to_file": exc_info}
    )

    return Response(
        data=Responses.error_response(message=error_message),
        status=EXCEPTION_STATUS_MAPPING.get(
            type(exception), status.HTTP_500_INTERNAL_SERVER_ERROR
        ),
    )


def handle_exceptions(view_func):
    """Decorator to handle exceptions and return appropriate HTTP responses."""

    def wrapper(request, *args, **kwargs):
        try:
            response = view_func(request, *args, **kwargs)
        except tuple(EXCEPTION_STATUS_MAPPING.keys()) as exception_class:
            response = handle_exception(exception_class)
        return response

    return wrapper
