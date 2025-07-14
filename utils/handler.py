"""
This module provides a method handler decorator to manage exceptions
and return standardized error responses.
"""

import logging
import time
from typing import Any, Callable

import psycopg2
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError

from utils.responses import Responses
from utils.strings import ResponseMessages

logger = logging.getLogger(__name__)


def method_handler(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to handle exceptions, log errors, and provide unified error responses."""

    def function_wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except IntegrityError as e:
            logger.error("IntegrityError: %s", e)
            return Responses.method_error_response(
                message=ResponseMessages.ALREADY_EXISTS.value, status_code=409
            )
        except ObjectDoesNotExist as e:
            logger.warning("ObjectDoesNotExist: %s", e)
            return Responses.method_error_response(
                message=ResponseMessages.NO_DATA_FOUND.value, status_code=404
            )
        except ValueError as e:
            logger.error("ValueError: %s", e)
            return Responses.method_error_response(
                message=ResponseMessages.INVALID_DATA.value, status_code=400
            )
        except psycopg2.Error as e:
            logger.critical("Database error: %s", e)
            return Responses.method_error_response(
                message=ResponseMessages.DATABASE_ERROR.value, status_code=500
            )
        except Exception as e:  # pylint: disable=broad-except
            logger.error("Unexpected error: %s", e)
            return Responses.method_error_response(
                message=ResponseMessages.GENERAL_ERROR.value, status_code=500
            )

    return function_wrapper


def log_execution(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to log the start and end of function execution."""

    def function_wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Starting function: {func.__name__}")
        logger.info("Starting function: %s", func.__name__)

        print(f"Arguments: {args}, {kwargs}")
        logger.info("Arguments: %s, %s", args, kwargs)

        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()

        duration = end_time - start_time

        print(f"Function {func.__name__} finished. Result: {result}")
        logger.info("Function %s finished. Result: %s", func.__name__, result)

        print(f"Execution time: {duration:.4f} seconds")
        logger.info("Execution time: %.4f seconds", duration)

        return result

    return function_wrapper


def retry(
    times: int, delay: float = 1
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """Decorator to retry a function `times` times with `delay` seconds between retries."""

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        def function_wrapper(*args: Any, **kwargs: Any) -> Any:
            attempts = 0
            while attempts < times:
                try:
                    return func(*args, **kwargs)
                except Exception as e:  # pylint: disable=broad-except
                    logger.warning(
                        "Error in %s: %s, retrying %d/%d",
                        func.__name__,
                        e,
                        attempts + 1,
                        times,
                    )
                    attempts += 1
                    time.sleep(delay)
            logger.error("Function %s failed after %d retries", func.__name__, times)
            raise RuntimeError(f"Function {func.__name__} failed after {times} retries")

        return function_wrapper

    return decorator


def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """Decorator to measure and log execution time of a function."""

    def function_wrapper(*args: Any, **kwargs: Any) -> Any:
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(
            "Function %s executed in %.4f seconds", func.__name__, execution_time
        )
        print("Function %s executed in %.4f seconds", {func.__name__}, {execution_time})
        return result

    return function_wrapper
