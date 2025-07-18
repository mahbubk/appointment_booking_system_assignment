"""
This module contains a utility class for generating consistent
API responses with success, error, and general response structures.
"""

from typing import Any, Optional


class Responses:
    """
    Utility class containing methods for generating API responses with a consistent format.
    """

    @staticmethod
    def success_response(
        is_success: bool = True, message: str = None, data: Optional[Any] = None
    ) -> dict:
        """
        Generates a success response dictionary with specified parameters.
        Args:
            is_success (bool): A flag indicating whether the response is a success or failure.
            Message (str): An optional message providing additional information.
            Data (dict): Additional data to include in the response.
        Returns:
            dict: The success response dictionary.
        """
        return {"is_success": is_success, "message": message, "data": data}

    @staticmethod
    def error_response(is_success: bool = False, message: str | dict = None) -> dict:
        """
        Generates an error response dictionary with specified parameters.
        Args:
            is_success (bool): A flag indicating whether the response is a success or failure.
            Message (str): An optional error message providing details about the failure.
        Returns:
            dict: The error response dictionary.
        """
        return {"is_success": is_success, "message": message, "data": None}

    @staticmethod
    def get_response(
        is_success: bool = True, message: bool = None, data: dict = None
    ) -> dict:
        """
        Generates a general response dictionary with specified parameters.
        Args:
            is_success (bool): A flag indicating whether the response is a success or failure.
            Message (str): An optional message providing additional information.
            Data (dict): Additional data to include in the response.
        Returns:
            dict: The response dictionary.
        """
        return {"is_success": is_success, "message": message, "data": data}

    @staticmethod
    def get_args(
        toast_type=None,
        toast_message="",
        user_name=None,
        is_success=None,
        profile_image_path=None,
    ) -> dict:
        """Generates a dictionary with various optional
        arguments for configuring and customizing responses."""
        return {
            "toast_type": toast_type,
            "toast_message": toast_message,
            "user_name": user_name,
            "is_success": is_success,
            "profile_image_path": profile_image_path,
        }

    @classmethod
    def method_error_response(cls, message: str, status_code: int = 400) -> dict:
        """
        Generate a standardized error response.

        Args:
            message (str): The error message to return. status_code (int, optional):
            The HTTP status code to return. Defaults to 400.
            status_code (int, optional): The HTTP status code to return. Defaults to 400.

        Returns:
            dict: A dictionary containing the error response
            with a status, message, and status code.
        """
        return {"status": "error", "message": message, "status_code": status_code}
