"""
Module: strings.py
This module defines a class containing constant strings used in the Auth Service API.
"""

from enum import Enum


class Strings:
    """
    Class containing constant strings used in the Auth Service API.
    """

    TOKEN_SECRET_KEY = "Assignment"
    API_NAME = "Appointment Booking System"
    API_VERSION = "v-0.0.1"
    API_DESCRIPTION = "This API is only for Client Authentication and Authorization"
    TERMS_OF_SERVICE = "https://appoint.com/"
    CONTACT_EMAIL = "appoitment@gmail.com"
    LICENSE = "BSD License"

    NO_DATA_FOUND = "No data found!"
    INSERTION_FAILED = "Could not insert data!"
    UPDATE_FAILED = "Could not update data!"
    DELETE_FAILED = "Could not delete data!"
    ALREADY_EXISTS = "Data already exists!"
    REQUEST_NONE = "Request is None!"
    TOKEN_EXPIRED = "Token expired!!"
    REFRESH_TOKEN_EXPIRED = "Refresh Token expired!"
    TOKEN_INVALID = "Token expired."
    TOKEN_MISSING = "Access token is missing."
    UNAUTHORIZED_TOKEN = "Unauthorized token."
    REFRESH_TOKEN_NOT_ALLOWED = "Refresh tokens are not allowed for this operation."

    PERMISSION_DENIED = "You do not have permission to access this resource."
    AUTH_ERROR = "Authentication credentials were not provided."
    REQUEST_SUCCESSFUL = "Request successful."
    REQUEST_FAILED = "Request failed!."
    INVALID_CREDENTIALS = "Invalid credentials"
    INACTIVE_USER = "Sorry, your account has been deactivated."
    EXCEPTION_MESSAGE = "Something went wrong! Please try again later."

    DAYS_OF_WEEK = (
        (0, "Sunday"),
        (1, "Monday"),
        (2, "Tuesday"),
        (3, "Wednesday"),
        (4, "Thursday"),
        (5, "Friday"),
        (6, "Saturday"),
    )

    @classmethod
    def get_api_info(cls) -> dict:
        """
        Get information about the API.

        Returns:
            dict: A dictionary containing information about the API.
        """
        return {
            "name": cls.API_NAME,
            "version": cls.API_VERSION,
            "description": cls.API_DESCRIPTION,
            "terms_of_service": cls.TERMS_OF_SERVICE,
            "contact_email": cls.CONTACT_EMAIL,
            "license": cls.LICENSE,
        }

    @classmethod
    def get_error_message(cls, error_code: str) -> str:
        """
        Get an error message for a specific error code.

        Args:
            error_code (str): The error code, e.g., 'NO_DATA_FOUND', 'INSERTION_FAILED', etc.

        Returns:
            str: The corresponding error message.
        """
        error_messages = {
            "NO_DATA_FOUND": cls.NO_DATA_FOUND,
            "INSERTION_FAILED": cls.INSERTION_FAILED,
            "UPDATE_FAILED": cls.UPDATE_FAILED,
            "DELETE_FAILED": cls.DELETE_FAILED,
            "ALREADY_EXISTS": cls.ALREADY_EXISTS,
            "TOKEN_EXPIRED": cls.TOKEN_EXPIRED,
        }

        return error_messages.get(error_code, "Unknown error")

    @classmethod
    def get_exception_message(cls) -> str:
        """
        Get the generic exception message.

        Returns:
            str: The generic exception message.
        """
        return cls.EXCEPTION_MESSAGE


class ResponseMessages(Enum):
    """
    Enumeration for various error messages used in the application.

    This Enum contains standardized messages that can be used for error handling
    and user feedback throughout the application.
    """

    NO_DATA_FOUND = "No data found!"
    INSERTION_FAILED = "Could not insert data!"
    UPDATE_FAILED = "Could not update data!"
    DELETE_FAILED = "Could not delete data!"
    ALREADY_EXISTS = "Data already exists!"
    REQUEST_NONE = "Request is None!"
    TOKEN_EXPIRED = "Token expired!"
    REFRESH_TOKEN_EXPIRED = "Refresh Token expired!"
    TOKEN_INVALID = "Token expired!"
    TOKEN_MISSING = "Access token is missing."
    UNAUTHORIZED_TOKEN = "Unauthorized token."
    REFRESH_TOKEN_NOT_ALLOWED = "Refresh tokens are not allowed for this operation."
    PERMISSION_DENIED = "You do not have permission to access this resource."
    AUTH_ERROR = "Authentication credentials were not provided."
    REQUEST_SUCCESSFUL = "Request successful."
    REQUEST_FAILED = "Request failed!"
    INVALID_CREDENTIALS = "Invalid credentials"
    INACTIVE_USER = "Sorry, your account has been deactivated."
    EXCEPTION_MESSAGE = "Something went wrong! Please try again later."
    INVALID_DATA = "Invalid data provided."
    DATABASE_ERROR = "Database error occurred."
    GENERAL_ERROR = "An error occurred."
    DELETE_SUCCESSFUL = "Data deleted successfully."
    ERROR_DATE_IN_PAST = "The provided date cannot be in the past."
    ERROR_SLOT_NOT_AVAILABLE = "Appointment slot is not available."

    ERROR_SAME_START_END_TIME = "Start time and end time cannot be the same"
    ERROR_INVALID_START_END_TIME = "Invalid start_time or end_time format"
    ERROR_START_TIME_BEFORE_END_TIME = "Start time must be before end time"
