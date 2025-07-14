"""
This module contains various utilities for authentication and token handling.

It includes imports for date and time operations, password hashing, and JSON Web Tokens.
Importing the ClientUser and Token models for user and token management in the auth_app.
"""

import datetime
from dataclasses import dataclass
from typing import Any, Dict, Union

import bcrypt
import jwt
import psycopg2
from django.core.exceptions import ObjectDoesNotExist
from user_agents import parse

from appointment_booking_system_app.db_cache import DbCache
from appointment_booking_system_app.models import Token, User
from utils.sql_helper import SqlHelper
from utils.strings import Strings

# pylint: disable=import-error


@dataclass
class Authentication:
    """Class for user authentication and token generation."""

    def __init__(self):
        self.db_cache = DbCache()
        self.sql_helper = SqlHelper()

    password: Union[str, None] = None

    @classmethod
    def generate_access_token(cls, user: User) -> str:
        """
        Generate an access token for a given user.

        Args:
            user (User): The user object.

        Returns:
            str: The access token as a JWT string.
        """
        if user is None:
            raise ValueError("User must be provided")

        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=0, hours=24, minutes=0, seconds=0),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "token_type": "access",
        }
        return jwt.encode(payload, Strings.TOKEN_SECRET_KEY, algorithm="HS256")

    @classmethod
    def generate_refresh_token(cls, user: User) -> str:
        """
        Generate a refresh token for a given user.

        Args:
            user (User): The user object.

        Returns:
            str: The refresh token as a JWT string.
        """

        if user is None:
            raise ValueError("User must be provided")

        payload = {
            "user_id": user.id,
            "username": user.username,
            "exp": datetime.datetime.now(datetime.timezone.utc)
            + datetime.timedelta(days=7, hours=0, minutes=0, seconds=0),
            "iat": datetime.datetime.now(datetime.timezone.utc),
            "token_type": "refresh",
        }
        return jwt.encode(payload, Strings.TOKEN_SECRET_KEY, algorithm="HS256")

    def create_access_token_from_refresh_token(
        self, refresh_token: str, fingerprint
    ) -> str | tuple:
        """
        Create a new access token from a refresh token.

        Args: refresh_token (str): The refresh token as a JWT string.
        Returns:The new access token as a JWT string, or None if the refresh token is invalid.
        """
        try:
            payload = jwt.decode(
                refresh_token, Strings.TOKEN_SECRET_KEY, algorithms=["HS256"]
            )
            if "token_type" in payload and payload["token_type"] == "refresh":
                payload = jwt.decode(
                    refresh_token, Strings.TOKEN_SECRET_KEY, algorithms=["HS256"]
                )
                user_id = payload["user_id"]

                user = User.objects.get(id=user_id)
                new_access_token = self.generate_access_token(user)
                new_refresh_token = self.generate_refresh_token(user)
                token = Token.objects.get(user_id=user_id)
                DbCache().delete_token(user_id=user_id)
                token = Token.objects.create(
                    user=user,
                    refresh_token=refresh_token,
                    access_token=new_access_token,
                    user_agent=fingerprint["browser"],
                    ip_address=fingerprint["user_ip"],
                    platform=fingerprint["platform"],
                )

                DbCache().set_cache(token.id, new_access_token, user_id)
                return new_access_token, new_refresh_token
            raise ValueError("Invalid token type")
        except (jwt.ExpiredSignatureError, jwt.DecodeError, ObjectDoesNotExist):
            return "Token validation failed."

    def set_password(self, raw_password: str) -> str:
        """
        Set the hashed password based on the provided raw password.

        Args:
            raw_password (str): The raw password.

        Returns:
            None
        """

        self.password = bcrypt.hashpw(
            raw_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        return self.password

    def check_password(stored_password: str, raw_password: str) -> bool:
        """
        Check if the provided raw password matches the stored hashed password.

        Args:
            stored_password (str): The stored hashed password.
            raw_password (str): The raw password.

        Returns:
            bool: True if the password is correct, False otherwise.
        """
        return bcrypt.checkpw(
            raw_password.encode("utf-8"), stored_password.encode("utf-8")
        )

    @staticmethod
    def get_browser_fingerprint(request) -> Dict[str, Union[str, None]]:
        """
        Get the browser fingerprint information from the request.
        Args:
            request: The request object containing user
            agent and IP address information.
        Returns:
            dict: A dictionary containing the user's browser fingerprint information.
                  Keys include 'user_ip', 'browser', and 'platform'.
                  Values may be strings or None if the information is not available.
        """
        user_ip = request.META.get("REMOTE_ADDR")
        user_agent_string = request.META.get("HTTP_USER_AGENT")
        user_agent = parse(user_agent_string)
        browser = user_agent.browser.family
        platform = user_agent.os.family

        return {
            "user_ip": user_ip,
            "browser": browser,
            "platform": platform,
        }

    @staticmethod
    def get_current_user(access_token) -> dict[str, Any] | None:
        """
        Retrieve the current user based on the provided access token.

        Args:
            access_token (str): The access token used
            to decode and retrieve the current user.

        Returns:
            dict[str, Any] or None: A dictionary
            containing user information if the user is found,
            None if the user is not found or an error occurs.
        """

        payload = jwt.decode(
            access_token, Strings.TOKEN_SECRET_KEY, algorithms=["HS256"]
        )
        if "token_type" in payload and payload["token_type"] == "access":
            payload = jwt.decode(
                access_token, Strings.TOKEN_SECRET_KEY, algorithms=["HS256"]
            )
        try:
            user_id = payload["user_id"]
            if user_id:
                user = User.objects.get(id=user_id)
                return user
            return None
        except psycopg2.Error as e:
            print(f"Error retrieving from cache: {e}")
            return None
