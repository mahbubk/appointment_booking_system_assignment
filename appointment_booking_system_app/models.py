"""
Defines the core data models for user roles and activity in the appointment booking system.

Includes:
- Administrative units: Division, District, Thana
- User model with role-based access

Each model maps to a database table and includes relationships for structured querying.
"""

from django.db import models


class Division(models.Model):
    """Represents a top-level administrative division (e.g., a state or province)."""

    name = models.TextField()

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.name)


class District(models.Model):
    """Represents a subdivision within a Division."""

    name = models.TextField()
    division = models.ForeignKey(Division, on_delete=models.CASCADE)

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.name)


class Thana(models.Model):
    """Represents a police precinct within a District."""

    name = models.TextField()
    district = models.ForeignKey(District, on_delete=models.CASCADE)

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.name)


class User(models.Model):
    """
    Custom user model representing different roles in the system (Admin, Doctor, Patient).

    Users can be associated with specific administrative regions like Division, District, and Thana.
    """

    ROLE_TYPE_CHOICES = [
        ("ADMIN", "Admin"),
        ("DOCTOR", "Doctor"),
        ("PATIENT", "Patient"),
    ]

    full_name = models.TextField()
    password = models.TextField()
    email = models.TextField(unique=True, db_index=True)
    phone = models.TextField(unique=True, db_index=True)
    profile_picture = models.TextField(blank=True)
    user_type = models.CharField(max_length=10, choices=ROLE_TYPE_CHOICES)
    division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, null=True, blank=True
    )

    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True
    )
    thana = models.ForeignKey(Thana, on_delete=models.SET_NULL, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.full_name)
