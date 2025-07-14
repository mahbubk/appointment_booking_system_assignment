"""
This module defines the repository and service classes for managing
CreditPackage data access and operations in the financial application.

It includes:
- `GenericRepository`: A generic repository for handling CRUD operations
  for any Django model.
- `CreditPackageRepository`: A repository specifically for managing
  CreditPackage instances.
"""

from typing import Generic, List, Optional, TypeVar

from django.core.exceptions import ObjectDoesNotExist

from appointment_booking_system_app.repository.repository import IRepository

T = TypeVar("T")


class GenericRepository(IRepository[T]):
    """Generic repository for managing data access and operations for any model."""

    def __init__(self, model: T):
        self.model = model

    def get_all(self, order_by: Optional[List[str]] = None) -> List[T]:
        """Retrieve all instances of the model, optionally ordered."""
        queryset = self.model.objects.all()
        if order_by:
            queryset = queryset.order_by(*order_by)
        return list(queryset)

    def get_by_id(self, primary_key: int) -> Optional[T]:
        """Retrieve a specific instance by primary key."""
        try:
            return self.model.objects.get(pk=primary_key)
        except ObjectDoesNotExist:
            return None

    def create(self, data: dict) -> T:
        """Create a new instance."""
        instance = self.model(**data)
        instance.save()
        return instance

    def update(self, instance: T, data: dict) -> T:
        """Update an existing instance."""
        for attr, value in data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

    def partial_update(self, instance: T, data: dict) -> T:
        """Partially update an existing instance."""
        for attr, value in data.items():
            if hasattr(instance, attr):
                setattr(instance, attr, value)
        instance.save()
        return instance

    def delete(self, instance: T) -> None:
        """Delete a specific instance."""
        instance.delete()


class GenericService(Generic[T]):
    """Generic service that uses the repository interface for operations."""

    def __init__(self, repository: IRepository[T]):
        self.repository = repository

    def get_all(self, order_by: Optional[List[str]] = None) -> List[T]:
        """Retrieve all instances of the model, optionally ordered."""
        return self.repository.get_all(order_by=order_by)

    def get_by_id(self, pk: int) -> Optional[T]:
        """Retrieve an instance by the primary key."""
        return self.repository.get_by_id(pk)

    def create(self, data: dict) -> T:
        """Create a new instance."""
        return self.repository.create(data)

    def update(self, instance: T, data: dict) -> T:
        """Update an existing instance."""
        return self.repository.update(instance, data)

    def partial_update(self, instance: T, data: dict) -> T:
        """Partially update an existing instance."""
        return self.repository.partial_update(instance, data)

    def delete(self, instance: T) -> None:
        """Delete a specific instance."""
        self.repository.delete(instance)
