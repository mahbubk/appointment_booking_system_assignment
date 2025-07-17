"""
Middleware to log all HTTP requests and responses.

- 2xx & 3xx responses logged at INFO level
- 4xx responses logged at WARNING level
- 5xx responses logged at ERROR level
"""

import logging

from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger("request_logger")


# pylint: disable=too-few-public-methods
class RequestLoggingMiddleware(MiddlewareMixin):
    """
    Logs every HTTP request and response status code
    with the appropriate log level based on status.
    """

    @staticmethod
    def process_response(request, response):
        """
        Called after the view is processed.
        Logs method, path, and status code.
        """
        method = request.method
        path = request.get_full_path()
        status_code = response.status_code

        log_message = f"{method} {path} → {status_code}"

        if 200 <= status_code < 400:
            logger.info(log_message)
        elif 400 <= status_code < 500:
            logger.warning(log_message)
        else:
            logger.error(log_message)

        return response
