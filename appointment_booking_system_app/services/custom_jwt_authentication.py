"""
Custom authentication module for handling JWT-based authentication.

This module defines two classes, `CustomJWTAuthentication` and `AllowAnyCustom`,
which are used to manage user authentication within the application.

Classes:
    CustomJWTAuthentication: Authenticates users based on JWT tokens.
    AllowAnyCustom: Allows any request to bypass authentication.

Usage:
    Use `CustomJWTAuthentication` as the default authentication class in views
    that require JWT authentication. Decorate views with `@AllowAnyCustom.allow_any`
    to bypass authentication.
"""

import datetime
import hmac
import threading
from hmac import compare_digest
from typing import Callable

import jwt
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response

from appointment_booking_system_app.db_cache import DbCache
from appointment_booking_system_app.models import User
from utils.api_utils import ApiUtils
from utils.responses import Responses
from utils.strings import ResponseMessages, Strings

_thread_locals = threading.local()


class CustomJWTAuthentication(BaseAuthentication):
    """
    Custom JWT authentication class for
    handling token-based authentication.
    """

    def authenticate(self, request):
        """
        Authenticates a user based on a JWT
        token provided in the request headers.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Optional[Tuple[Dict, str]]: Returns a tuple containing user
            information and token if authentication is successful, else None.

        Raises:
            AuthenticationFailed: If the token is missing, expired, or invalid.
        """

        token = request.headers.get("Api-Key")
        if not token or compare_digest(token, ""):
            raise AuthenticationFailed(Strings.TOKEN_MISSING)
        is_expired, user_id = ApiUtils.is_access_token_expired(token)
        if is_expired:
            raise AuthenticationFailed(Strings.TOKEN_EXPIRED)
        cached_token = DbCache().get_token(user_id)
        try:
            if not hmac.compare_digest(token, cached_token):
                raise AuthenticationFailed(Strings.TOKEN_INVALID)
        except TypeError as exc:
            raise AuthenticationFailed(Strings.TOKEN_INVALID) from exc
        try:
            payload = jwt.decode(token, Strings.TOKEN_SECRET_KEY, algorithms=["HS256"])
            user = User.objects.get(id=user_id)

            if payload["token_type"] == "access" and datetime.datetime.now(
                datetime.timezone.utc
            ) > datetime.datetime.fromtimestamp(payload["exp"], datetime.timezone.utc):
                raise AuthenticationFailed(Strings.TOKEN_INVALID)
            if payload["token_type"] == "refresh":
                raise AuthenticationFailed(Strings.REFRESH_TOKEN_NOT_ALLOWED)
            CustomJWTAuthentication().set_current_user(user)
            return user, token
        except (
            jwt.DecodeError,
            jwt.ExpiredSignatureError,
            jwt.InvalidTokenError,
        ) as exc:
            raise AuthenticationFailed(ResponseMessages.TOKEN_INVALID.value) from exc
        except ObjectDoesNotExist as exc:
            raise AuthenticationFailed(ResponseMessages.NO_DATA_FOUND.value) from exc
        except Exception as exc:
            raise AuthenticationFailed(ResponseMessages.TOKEN_INVALID.value) from exc

    @classmethod
    def jwt_authenticated(cls, func: Callable) -> Callable:
        """
        Decorator to enforce JWT authentication on view functions.

        Args:
            func (Callable): The function to decorate.

        Returns:
            Callable: The wrapped function with JWT authentication applied.
        """

        def wrapper(request, *args, **kwargs):
            auth_instance = cls()
            try:
                user, token = auth_instance.authenticate(request)
                if user is not None and token is not None:
                    if user.is_active:
                        return func(request, *args, **kwargs)
                    return Response(
                        data=Responses.error_response(
                            message=ResponseMessages.INACTIVE_USER.value,
                        ),
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            except AuthenticationFailed as e:
                return Response(
                    data=Responses.error_response(
                        message=e.detail if hasattr(e, "detail") else None
                    ),
                    status=status.HTTP_401_UNAUTHORIZED,
                )
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.TOKEN_INVALID.value,
                ),
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return wrapper

    @classmethod
    def get_current_user(cls):
        """
        Retrieves the current authenticated
        user from thread-local storage.

        Returns:
            Optional[str]: The username of
            the current user or None if not set.
        """

        return getattr(_thread_locals, "user", None)

    @classmethod
    def set_current_user(cls, user):
        """
        Sets the current authenticated
        user in thread-local storage.

        Args:
            user (dict): The user object
            containing user information.
        """

        _thread_locals.user = user.id


class AllowAnyCustom(BaseAuthentication):
    """
    Custom authentication class that allows any request by bypassing
    authentication entirely. Useful for public endpoints or views
    that do not require user authentication.
    """

    def authenticate(self, request):
        """
        Overrides the authenticate method to allow any request.

        Args:
            request (Request): The incoming HTTP request.

        Returns:
            Tuple[None, None]: Always returns
            (None, None) to bypass authentication.
        """

        return None, None

    @classmethod
    def allow_any(cls, func: Callable) -> Callable:
        """
        Decorator to allow any request without authentication.

        Args:
            func (Callable): The function to decorate.

        Returns:
            Callable: The wrapped function
            with no authentication enforcement.
        """

        def wrapper(request, *args, **kwargs):
            auth = cls()
            auth.authenticate(request)
            _thread_locals.user = None
            return func(request, *args, **kwargs)

        return wrapper
