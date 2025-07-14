"""
Module for managing database caching using psycopg2 and SqlHelper.
"""

import json

import psycopg2
from django.core.exceptions import ObjectDoesNotExist

from appointment_booking_system_app.models import CacheToken, Token


class DbCache:
    """Class for managing a cache in an SQL database."""

    @staticmethod
    def set_cache(token_key, access_token, user_id):
        """
        insert a cache entry into the database.
        Args:
            token_key (str): The key associated with the access token.
            access_token (str): The access token to be cached.
            user_id (int): The user ID associated with the access token.
        """
        try:
            CacheToken.objects.create(
                token_key=token_key, access_token=access_token, user_id=user_id
            )
        except psycopg2.Error as exe:
            print(f"Error inserting into cache: {exe}")

    @staticmethod
    def get_token(user_id):
        """
        Retrieve a cached access token from the database.
        Args:
            user_id (str): The user id to be retrieved.
        Returns:
            str or None: The retrieved access token
            from recruiting models imports CacheToken, Token or None if not found.
        """
        try:
            token = CacheToken.objects.filter(user_id=user_id).last()
            if token:
                return token.access_token
            return None
        except ObjectDoesNotExist:
            error_response = {"error": "Token not found"}
            return json.dumps(error_response)
        except psycopg2.Error as exe:
            print(f"Error retrieving from cache: {exe}")
            error_response = {"error": "Internal server error"}
            return json.dumps(error_response)

    @staticmethod
    def delete_token(user_id=None):
        """
        delete cache entries from the database based on token ID or user ID.
        Args:
            user_id (int, optional): The user ID whose entries are to be deleted.
                if None, entries associated with the token ID will be deleted.
        Note:
            At least one of token_id or user_id must be provided.
        """
        try:
            cache_token = CacheToken.objects.filter(user_id=user_id)
            token = Token.objects.filter(user_id=user_id)
            if cache_token.exists():
                cache_token.delete()
            if token.exists():
                token.delete()
        except psycopg2.Error as exe:
            print(f"Error deleting from cache: {exe}")
