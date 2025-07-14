"""
Provides functions for encoding and decoding binary data as ASCII text.

Provides classes for working with dates and times,
Provides functions for interacting with the operating system,
Generates universally unique identifiers (UUIDs),
Provides tools for creating decorators,
Implements JSON Web Tokens for secure communication,
Python Imaging Library for working with images,
Part of the Django REST framework for web APIs,
Part of the Django REST framework for handling API responses
"""
import datetime
import os
from dataclasses import dataclass
from typing import Any

import jwt
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import DatabaseError
from django.utils import timezone
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from appointment_booking_system_app.db_cache import DbCache
from appointment_booking_system_app.models import Token
from appointment_booking_system_app.services.authentication import Authentication

from .responses import Responses
from .strings import Strings

# pylint: disable=import-error


@dataclass
class ApiUtils:
    """
    Utility class containing various methods for handling API-related tasks.

    Create an in-memory dictionary to store valid access tokens and their
    associated user information.
    """

    db_cache = DbCache()
    auth = Authentication()

    @classmethod
    def _unauthorized_response(cls):
        """Generate standard 401 Unauthorized response.

        Returns:
            Response: Django REST Framework response with status 401
        """
        return Response(
            data=Responses.error_response(message=Strings.AUTH_ERROR),
            status=status.HTTP_401_UNAUTHORIZED,
        )

    @classmethod
    def _permission_denied_response(cls):
        """Generate standard 403 Forbidden response.

        Returns:
            Response: Django REST Framework response with 403 status
        """
        return Response(
            data=Responses.error_response(message=Strings.PERMISSION_DENIED),
            status=status.HTTP_403_FORBIDDEN,
        )

    @classmethod
    def get_user(cls, request) -> dict[str, Any] | Response:
        """
        Decorator to check if the current user has the required permission roles.
        Returns:
            function: The decorated view function.
        """

        access_token = request.headers.get("Api-Key")
        current_user = cls.auth.get_current_user(access_token)
        if current_user:
            return current_user
        return Response(
            data=Responses.error_response(message=Strings.NO_DATA_FOUND),
            status=status.HTTP_404_NOT_FOUND,
        )

    @classmethod
    def generate_and_store_tokens(cls, user, fingerprint):
        """
        generate new access and refresh tokens for the user,
        delete existing tokens for the same user and platform,
        and store the new tokens in the database.

        Args:
            user: The user for whom tokens are generated.
            fingerprint (dict): A dictionary containing browser,
            user_ip, and platform information.

        Returns:
            str: The generated access token.
            str: The generated refresh token.
        """
        DbCache.delete_token(user.id)

        access_token = cls.auth.generate_access_token(user)
        refresh_token = cls.auth.generate_refresh_token(user)

        token = Token.objects.create(
            user=user,
            refresh_token=refresh_token,
            access_token=access_token,
            user_agent=fingerprint["browser"],
            ip_address=fingerprint["user_ip"],
            platform=fingerprint["platform"],
        )
        try:
            cls.db_cache.set_cache(token.id, access_token, user.id)
        except (KeyError, TypeError, ValueError) as e:
            print(f"Token caching failed: {e}")
        return access_token, refresh_token

    @classmethod
    def get_user_token_count(cls, user_id):
        """View to get the total number of tokens for a given user."""
        user_tokens_count = Token.objects.filter(user_id=user_id).count()
        return user_tokens_count

    @classmethod
    def delete_tokens_with_same_user_and_platform(cls, user_id):
        """
        delete tokens where the user ID and platform are the same.

        Args:
            user_id (int): The ID of the user.

        Returns:
            int: The number of tokens deleted.
        """
        try:
            tokens_to_delete = Token.objects.filter(user_id=user_id)
            num_deleted, _ = tokens_to_delete.delete()
            return num_deleted
        except DatabaseError as e:
            print("Database error deleting tokens:", e)
            return 0

    @classmethod
    def is_access_token_expired(cls, access_token):
        """
        Check the validity of an access token.

        Args:
            access_token (str): The access token to check.

        Returns:
            bool: True if the access token is valid, False otherwise.
        """
        try:
            payload = jwt.decode(
                access_token, Strings.TOKEN_SECRET_KEY, algorithms=["HS256"]
            )
            exp = payload.get("exp")
            if exp is None:
                return True, None

            if datetime.datetime.now(
                datetime.timezone.utc
            ) > datetime.datetime.fromtimestamp(payload["exp"], datetime.timezone.utc):
                return True, None
            user_id = payload.get("user_id")
            return False, user_id
        except jwt.ExpiredSignatureError:
            return True, None
        except jwt.DecodeError:
            return True, None

    @classmethod
    def is_refresh_token_expired(cls, refresh_token):
        """
        Check the validity of an access token.

        Args:
            refresh_token (str): The access token to check.

        Returns:
            bool: True if the access token is valid, False otherwise.
        """
        try:
            payload = jwt.decode(
                refresh_token, Strings.TOKEN_SECRET_KEY, algorithms=["HS256"]
            )
            if datetime.datetime.now(
                datetime.timezone.utc
            ) > datetime.datetime.fromtimestamp(payload["exp"], datetime.timezone.utc):
                return True
            refresh_token_exists = Token.objects.filter(
                refresh_token=refresh_token
            ).exists()
            return refresh_token_exists, False
        except jwt.ExpiredSignatureError:
            return False, True
        except jwt.DecodeError:
            return False, True

    @classmethod
    def check_access_token_validity(cls, token_id):
        """View to check the expiration validity of an access token."""
        try:
            token = Token.objects.get(pk=token_id)
            if not cls.is_access_token_expired(token.access_token):
                return True
            return Response(
                data=Responses.error_response(message=Strings.TOKEN_EXPIRED),
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except ObjectDoesNotExist:
            return Response(
                data=Responses.error_response(message=Strings.TOKEN_MISSING),
                status=status.HTTP_404_NOT_FOUND,
            )

    @staticmethod
    def handle_exceptions(view_func):
        """Decorator to handle exceptions and return appropriate HTTP responses.

        Maps common exceptions to HTTP status codes and formats consistent error responses.
        Handles:
        - ValueError: 400 Bad Request
        - ObjectDoesNotExist: 400 Bad Request
        - ValidationError: 422 Unprocessable Entity
        - APIException: 400 Bad Request
        - All other exceptions: 500 Internal Server Error
        """
        exception_mapping = {
            ValueError: status.HTTP_400_BAD_REQUEST,
            ObjectDoesNotExist: status.HTTP_400_BAD_REQUEST,
            ValidationError: status.HTTP_422_UNPROCESSABLE_ENTITY,
            APIException: status.HTTP_400_BAD_REQUEST,
            Exception: status.HTTP_500_INTERNAL_SERVER_ERROR,
        }

        def wrapper(request, *args, **kwargs):
            try:
                return view_func(request, *args, **kwargs)
            except tuple(exception_mapping.keys()) as e:
                return _create_error_response(e, exception_mapping)

        def _create_error_response(exception, mapping):
            """Create a standardized error response from exception."""
            error_message = _extract_error_message(exception)
            status_code = mapping.get(
                type(exception), status.HTTP_500_INTERNAL_SERVER_ERROR
            )
            return Response(
                data=Responses.error_response(message=error_message), status=status_code
            )

        def _extract_error_message(exception):
            """Extract and format error message from exception."""
            if isinstance(exception, APIException):
                message = exception.detail
            elif hasattr(exception, "message"):
                message = exception.message
            else:
                message = str(exception)

            if isinstance(message, dict) and "detail" in message:
                message = message["detail"]
            elif isinstance(message, list):
                message = message[0] if message else "An error occurred"

            return message

        return wrapper

    @staticmethod
    def format_mobile_number(mobile_number: str) -> str:
        """
        Format a mobile number to include a country code if it doesn't start with it.

        Args:
            mobile_number (str): The mobile number.

        Returns:
            str: The formatted mobile number.
        """

        mobile_number = str(mobile_number).strip()

        if not mobile_number.startswith("+88"):
            mobile_number = f"+88{str(mobile_number).strip()}"

        return mobile_number

    @staticmethod
    def format_date_time(date: str) -> datetime:
        """
        Format a date and time string into a datetime object.

        Args:
            date (str): The date and time string in the format "%Y-%m-%d %H:%M".

        Returns:
            datetime.datetime: The formatted datetime object.
        """

        temp_date = datetime.datetime.strptime(date, "%Y-%m-%d %H:%M")
        year = temp_date.year
        month = temp_date.month
        day = temp_date.day
        hour = temp_date.hour
        minute = temp_date.minute

        return datetime.datetime(
            year=year, month=month, day=day, hour=hour, minute=minute
        )

    @staticmethod
    def generate_code(last_count: str) -> str:
        """
        Generate a code based on the last count value.

        Args:
            last_count (str or int): The last count value.

        Returns:
            str: The generated code.
        """

        last_count = int(str(last_count).replace("0", "")) if last_count else 0

        count = last_count + 1

        return str(count).zfill(5)

    @staticmethod
    def delete_image(file_path: str) -> None:
        """
        Delete an image file from the specified path.

        Args:
            file_path (str): The path to the image file to be deleted.
        """
        if os.path.exists(file_path):
            os.remove(file_path)
        else:
            print(f"File not found at path: {file_path}")

    @staticmethod
    def rename_image_file() -> str | None:
        """
        Generate a unique image file name using the current timestamp.

        Returns:
            str: A string representing the new image
            file name in the format 'YYYY-MM-DD-HHMMSS.jpg'.
        """
        new_file_name = f"{timezone.now().strftime('%Y%m%d%H%M%S')}.jpg"
        return new_file_name
