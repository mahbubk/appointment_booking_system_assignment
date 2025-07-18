"""
This module defines the repository and service classes for managing
Skills data access and operations.

It includes:
- GenericRepository: A generic repository for handling CRUD operations
  for any Django model.
- GenericService: A generic service interface for managing operations
  on any model using a repository pattern.
"""


from cfgv import ValidationError

from appointment_booking_system_app.models import User
from appointment_booking_system_app.repository.generic_repository import (
    GenericRepository,
    GenericService,
)
from appointment_booking_system_app.services.authentication import Authentication
from utils.sql_helper import SqlHelper

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
    related to Users instances, using the repository layer for
    database interactions.

    This class provides a layer of abstraction over the repository, allowing
    for the enforcement of additional validation rules, data transformations,
    and other business logic. It is designed to be used by application
    components that require access to Users' data while abstracting away
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

    def get_by_id(self, pk: int) -> User | None:
        """Retrieve an instance by primary key with validation."""
        if pk <= 0:
            raise ValidationError("Primary key must be a positive integer.")

        return self.repository.get_by_id(pk)


user_repository = UserRepository()
user_service = UserService(user_repository)
