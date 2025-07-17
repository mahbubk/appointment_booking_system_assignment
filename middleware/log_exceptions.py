"""
Custom logging filter to selectively include traceback information in file logs.

This filter checks if the log record has 'exc_info_to_file' attribute:
- If present, it sets 'record.exc_info' to that value (the real exception tuple)
  so that the traceback appears in file logs.
- Otherwise, it removes 'exc_info' so the traceback does not appear.

Useful for logging exceptions with traceback only in files
(e.g., error.log) while keeping console output clean.
"""

import logging


# pylint: disable=too-few-public-methods
class ExcInfoToFileFilter(logging.Filter):
    """
    Logging filter to add exception info to log records
    only when 'exc_info_to_file' is provided.

    Helps print tracebacks to file logs while avoiding them in the console.
    """

    def filter(self, record):
        exc_info_to_file = getattr(record, "exc_info_to_file", None)
        if exc_info_to_file:
            record.exc_info = exc_info_to_file
        else:
            record.exc_info = None
        return True
