"""
This module defines the repository and service classes for managing
Skills data access and operations in the financial application.

It includes:
- GenericRepository: A generic repository for handling CRUD operations
  for any Django model.
- GenericService: A generic service interface for managing operations
  on any model using a repository pattern.
"""

import base64
import imghdr
import time
from io import BytesIO
from typing import Any, List, Optional

from cfgv import ValidationError
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db.models import Model
from phonenumbers.phonenumberutil import format_number_for_mobile_dialing
from PIL import Image
from rest_framework import serializers, status
from rest_framework.response import Response

from appointment_booking_system_app.models import User
from appointment_booking_system_app.repository.generic_repository import (
    GenericRepository,
    GenericService,
    T,
)

from rest_framework.exceptions import ValidationError as DRFValidationError

from appointment_booking_system_app.serializers import UserSerializer
from appointment_booking_system_app.services.authentication import Authentication
from utils.api_utils import ApiUtils
from utils.sql_helper import SqlHelper
from utils.utils import validate_image_file, validate_password_strength

auth = Authentication()

sql_helper = SqlHelper()


class UserRepository(GenericRepository[User]):
    """Repository for managing Users data access and operations."""

    def __init__(self):
        """
        Initialize the Users.

        This constructor initializes the repository with the Users model,
        enabling CRUD operations on the Users instances.

        It calls the superclasses __init__ method with the Users model
        as an argument, allowing the generic repository functionality to be
        applied to the Users model specifically.
        """

        super().__init__(User)


class UserService(GenericService[User]):
    """
    Service class responsible for handling business logic and operations
    related to Users instances, utilizing the repository layer for
    database interactions.

    This class provides a layer of abstraction over the repository, allowing
    for the enforcement of additional validation rules, data transformations,
    and other business logic. It is designed to be used by application
    components that require access to Users data while abstracting away
    direct database operations.

    Key Responsibilities:
    - Retrieve, create, update, and delete Users instances by delegating
      these operations to the Users repository.
    - Implement and enforce business-specific validations and rules, such as
      validating input parameters for retrieval and update operations.
    - Serve as the main access point for Users-related operations within
      the application, ensuring consistent handling of Users data.

    Methods:
    - get_by_id: Retrieves a CreditPackage instance by primary key, with validation
      to ensure the key is a positive integer.
    - Additional CRUD methods inherited from GenericService.
    """

    @classmethod
    def validate_password_strength(cls, password):
        """
        Validate password strength using Django's built-in password validation.

        Args:
            password (str): The password to be validated.
        Raises:
            serializers.ValidationError: If the password does not meet the required strength.
        """
        try:
            validate_password_strength(password)
        except ValidationError as exe:
            raise serializers.ValidationError(exe) from exe  # type: ignore

    def create(self, data: dict) -> User | Any:
        """Create a User new instance."""

        profile_picture = data.pop("profile_picture")
        print(profile_picture)
        # password = data.pop("password")
        phone_number = data.pop("phone")

        # if password:
        #     validate_password_strength(password)
        #     password = auth.set_password(password)
        #     data["password"] = password

        if profile_picture:
            try:
                validate_image_file(profile_picture)
                data['profile_picture'] = profile_picture
            except ValidationError as e:
                raise serializers.ValidationError({'profile_picture': e.detail})

        if phone_number:
            data["phone"] = ApiUtils.format_mobile_number(phone_number)

        user_serializer = UserSerializer(data=data)

        if not user_serializer.is_valid():
            return Response(
                data={"errors": user_serializer.errors},
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = user_serializer.save()

        return user


user_repository = UserRepository()
user_service = UserService(user_repository)
