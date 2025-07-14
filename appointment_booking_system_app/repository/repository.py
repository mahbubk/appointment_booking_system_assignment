"""
This module contains an abstract base repository class and a generic repository class
for managing Django model data access and operations. The classes use type hints
to enforce model-specific typing and support CRUD operations for Django models.
"""

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from django.db import models

T = TypeVar("T", bound=models.Model)


class IRepository(ABC, Generic[T]):
    """Abstract base class for repository interface."""

    @abstractmethod
    def get_all(self, order_by: Optional[List[str]] = None) -> List[T]:
        """Retrieve all instances of the model."""

    @abstractmethod
    def get_by_id(self, primary_key: int) -> Optional[T]:
        """Retrieve a specific instance by primary key."""

    @abstractmethod
    def create(self, data: dict) -> T:
        """Create a new instance."""

    @abstractmethod
    def update(self, instance: T, data: dict) -> T:
        """Update an existing instance."""

    @abstractmethod
    def partial_update(self, instance: T, data: dict) -> T:
        """Partially update an existing instance."""

    @abstractmethod
    def delete(self, instance: T) -> None:
        """Delete a specific instance."""
