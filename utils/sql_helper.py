"""
This module contains classes and functions related
to database operations.
"""

from contextlib import contextmanager
from typing import Any, Dict, Optional, Protocol

from django.db import connection, connections
from psycopg2.extras import execute_values

from utils.handler import method_handler

# pylint: disable=E0401
from utils.responses import Responses
from utils.strings import ResponseMessages


class SQLHelperProtocol(Protocol):
    """
    A protocol that defines the SQL helper interface.

    This protocol is used for interacting with the database.
    Any class implementing this protocol must provide the `select_one` method.
    """

    def execute(self, query: str, values: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Executes an SQL query.

        Args:
            query (str): The SQL query to execute.
            values (tuple, optional): Values to be injected into the query.

        Returns:
            dict: A success response dictionary.
        """

    def insert(self, query: str, values: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Inserts a single record into the database.

        Args:
            query (str): The SQL query for insertion.
            values (tuple, optional): Values to be inserted.

        Returns:
            dict: A success response dictionary if insertion is successful,
                  otherwise an error response.
        """

    def bulk_insert(self, query: str, values: list) -> Dict[str, Any]:
        """
        Bulk inserts multiple records into the database.

        Args:
            query (str): The SQL query for bulk insertion.
            values (list): List of tuples representing values for bulk insertion.

        Returns:
            dict: A success response dictionary if bulk insertion is successful,
                  otherwise an error response.
        """

    def insert_with_id(
        self, query: str, values: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """
        Inserts a record into the database and returns the generated ID.

        Args:
            query (str): The SQL query for insertion.
            values (tuple, optional): Values to be inserted.

        Returns:
            dict: A success response dictionary with the generated ID if insertion
                  is successful, otherwise an error response.
        """

    def update(self, query: str, values: tuple) -> Dict[str, Any]:
        """
        Updates records in the database.

        Args:
            query (str): The SQL query for update.
            values (tuple): Values to be used in the update operation.

        Returns:
            dict: A success response dictionary if the update is successful,
                  otherwise an error response.
        """

    def select(self, query: str, values: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Executes a SELECT query and retrieves data from the database.

        Args:
            query (str): The SQL query for selection.
            values (tuple, optional): Values to be used in the query parameters.

        Returns:
            dict: A success response dictionary with the retrieved data if successful,
                  otherwise an error response.
        """

    def select_one(self, query: str, values: tuple) -> dict:
        """
        Executes a single-row select query on the database.

        Args:
            query (str): The SQL query to execute.
            values (tuple): The values to inject into the query.

        Returns:
            dict: The result of the query execution.
        """

    def delete(self, query: str, values: tuple) -> Dict[str, Any]:
        """
        Deletes records from the database.

        Args:
            query (str): The SQL query for deletion.
            values (tuple): Values to be used in the deletion operation.

        Returns:
            dict: A success response dictionary if deletion is successful,
                  otherwise an error response.
        """

    def delete_all(self, query: str) -> Dict[str, Any]:
        """
        Deletes all records based on the provided query.

        Args:
            query (str): The SQL query for deleting all records.

        Returns:
            dict: A success response dictionary if deletion is successful,
                  otherwise an error response.
        """


class SqlHelper:
    """
    A simple class representing a database connection with a cursor.

    Attributes:
        database_alias (str): The alias for the database connection.

    Methods:
        get_cursor: Context manager that provides a cursor for executing SQL queries.
        execute: Execute a given SQL query, optionally with parameters.
        insert: Insert a single record into the database using a provided SQL query.
        bulk_insert: Bulk insert multiple records into the database using a provided SQL query.
        insert_with_id: Insert a record into the database and return the generated ID.
        update: Update records in the database using a provided SQL query and parameters.
        select: Execute a SELECT query and retrieve multiple records from the database.
        select_one: Execute a SELECT query to retrieve a single record from the database.
        delete: Delete records from the database using a provided SQL query and parameters.
        delete_all: Delete all records based on the provided SQL query.
    """

    def __init__(self, database_alias="default"):
        self.database_alias = database_alias

    @contextmanager
    def get_cursor(self):
        """
        Context manager to yield a valid cursor object for executing SQL queries,
        ensuring proper handling of atomic blocks and non-atomic operations.
        """
        db_connection = connections[self.database_alias]

        if db_connection.in_atomic_block:
            with db_connection.cursor() as cursor:
                yield cursor
        else:
            with db_connection.cursor() as cursor:
                try:
                    yield cursor
                    db_connection.commit()
                except Exception as e:
                    db_connection.rollback()
                    raise e

    @method_handler
    def execute(self, query: str, values: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Execute an SQL query.
        Args:
            query (str): The SQL query to be executed.
            values (tuple, optional): Values to be used
            in the query parameters.
        Returns:
            dict: A success response dictionary.
        """
        with self.get_cursor() as cursor:
            if values is None:
                cursor.execute(
                    query,
                )
            else:
                cursor.execute(query, values)

            connection.commit()
            return Responses.success_response()

    @method_handler
    def insert(self, query: str, values: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Insert a single record into the database.
        Args:
            query (str): The SQL query for insertion.
            values (tuple, optional): Values to be inserted.
        Returns:
            dict: A success response dictionary if insertion
            is successful, otherwise an error response.
        """
        with self.get_cursor() as cursor:
            if values is None:
                cursor.execute(
                    query,
                )
            else:
                cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount == 1:
                return Responses.success_response()
            return Responses.error_response(
                message=ResponseMessages.INSERTION_FAILED.value
            )

    @method_handler
    def bulk_insert(self, query: str, values: list) -> Dict[str, Any]:
        """
        Bulk insert multiple records into the database.
        Args:
            query (str): The SQL query for bulk insertion.
            values (list): List of tuples representing values for bulk insertion.
        Returns:
            dict: A success response dictionary if bulk insertion
            is successful, otherwise an error response.
        """
        with self.get_cursor() as cursor:
            execute_values(cursor, query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return Responses.success_response()
            return Responses.error_response(
                message=ResponseMessages.INSERTION_FAILED.value
            )

    @method_handler
    def insert_with_id(
        self, query: str, values: Optional[tuple] = None
    ) -> Dict[str, Any]:
        """
        Insert a record into the database and return the generated ID.
        Args:
            query (str): The SQL query for insertion.
            values (tuple, optional): Values to be inserted.
        Returns:
            dict: A success response dictionary with the
            generated ID if insertion is successful,
            otherwise an error response.
        """
        with self.get_cursor() as cursor:
            if values is None:
                cursor.execute(
                    query,
                )
            else:
                cursor.execute(query, values)
            return_id = cursor.fetchone()

            if cursor.rowcount == 1:
                return Responses.success_response(data=return_id)
            return Responses.error_response(
                message=ResponseMessages.INSERTION_FAILED.value
            )

    @method_handler
    def update(self, query: str, values: tuple) -> Dict[str, Any]:
        """
        Update records in the database.
        Args:
            query (str): The SQL query for update.
            values (tuple): Values to be used in the update operation.
        Returns:
            dict: A success response dictionary if the update is successful,
            otherwise an error response.
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return Responses.success_response()
            return Responses.error_response(
                message=ResponseMessages.UPDATE_FAILED.value
            )

    @method_handler
    def select(self, query: str, values: Optional[tuple] = None) -> Dict[str, Any]:
        """
        Execute a SELECT query and retrieve data from the database.
        Args:
            query (str): The SQL query for selection.
            values (tuple, optional): Values to be used in the query parameters.
        Returns:
            dict: A success response dictionary with the retrieved data if successful,
                  otherwise an error response.
        The 'data' field in the response dictionary contains a list of dictionaries,
        where each dictionary represents a row of retrieved data.
        """
        with self.get_cursor() as cursor:
            if values is None:
                cursor.execute(
                    query,
                )
            else:
                cursor.execute(query, values)
            result = cursor.fetchall()

            row_headers = [col[0] for col in cursor.description]
            data = [dict(zip(row_headers, row)) for row in result]

            if len(data) > 0:
                return Responses.success_response(data=data)
            return Responses.error_response(
                message=ResponseMessages.NO_DATA_FOUND.value
            )

    @method_handler
    def select_one(self, query: str, values: tuple = None) -> Dict[str, Any]:
        """
        Execute a SELECT query to retrieve a single record.

        Args:
            query (str): The SQL query for selection.
            values (tuple, optional): Values to be used in the query parameters.

        Returns:
            dict: A success response dictionary with the retrieved data if successful,
                  otherwise an error response.
        """

        with self.get_cursor() as cursor:
            cursor.execute(query, values)

            result = cursor.fetchone()

            if result:
                row_headers = [col[0] for col in cursor.description]
                data = dict(zip(row_headers, result))
                return Responses.success_response(data=data)
            return Responses.error_response(
                message=ResponseMessages.NO_DATA_FOUND.value
            )

    @method_handler
    def delete(self, query: str, values: tuple) -> Dict[str, Any]:
        """
        Delete records from the database.
        Args:
            query (str): The SQL query for deletion.
            values (tuple): Values to be used in the deletion operation.
        Returns:
            dict: A success response dictionary if deletion is successful,
            otherwise an error response.
        """
        with self.get_cursor() as cursor:
            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                return Responses.success_response()
            return Responses.error_response(
                message=ResponseMessages.DELETE_FAILED.value
            )

    @method_handler
    def delete_all(self, query: str) -> Dict[str, Any]:
        """
        Delete all records based on the provided query.
        Args:
            query (str): The SQL query for deleting all records.
        Returns:
            dict: A success response dictionary if deletion is successful,
            otherwise an error response.
        """
        with self.get_cursor() as cursor:
            cursor.execute(
                query,
            )
            connection.commit()
            return Responses.success_response()
