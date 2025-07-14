"""
Defines the core data models for user roles and activity in the appointment booking system.

Includes:
- Administrative units: Division, District, Thana
- User model with role-based access

Each model maps to a database table and includes relationships for structured querying.
"""

from django.db import models


class Time(models.Model):
    """
    An abstract base model that provides timestamp and user tracking fields.

    Attributes:
        created_at (DateTimeField): The date and time when the record was created.
        Created_by (CharField): The user who created the record.
        Updated_at (DateTimeField): The date and time when the record was last updated.
        Updated_by (CharField): The user who last updated the record.
    :param created_at: The date and time when the record was created.
    :param created_by: The user who created the record.
    :param updated_at: The date and time when the record was last updated.
    :param updated_by: The user who last updated the record.
    """

    objects = None
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.CharField(max_length=50, default="dev")
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    updated_by = models.CharField(max_length=50, blank=True, default="")

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Meta-options for the Time model.

        This model is abstract and does not create a database table. It is intended
        to be inherited by other models to provide common fields for timestamping
        and user tracking. The `abstract` option is set to True to ensure this behavior.
        """

        abstract = True


class Division(models.Model):
    """Represents a top-level administrative division (e.g., a state or province)."""

    name = models.TextField()

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.name)


class District(models.Model):
    """Represents a subdivision within a Division."""

    name = models.TextField()
    division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.name)


class Thana(models.Model):
    """Represents a police precinct within a District."""

    name = models.TextField()
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.name)


class User(Time):
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
    email = models.EmailField(unique=True, db_index=True)
    phone = models.TextField(unique=True, db_index=True, max_length=14)
    profile_picture = models.ImageField(
        upload_to="profile_pictures/", null=True, blank=True
    )
    user_type = models.CharField(max_length=10, choices=ROLE_TYPE_CHOICES)
    division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, null=True, blank=True
    )

    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True
    )
    thana = models.ForeignKey(Thana, on_delete=models.SET_NULL, null=True, blank=True)
    license_number = models.TextField(blank=True)
    total_experience = models.TextField(blank=True)
    consultation_fee = models.TextField(blank=True)
    availability = models.TimeField(blank=True, null=True, default=None)
    is_active = models.BooleanField(
        default=True
    )  # True for active user and False for inactive user



    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.full_name)


class Token(Time):
    """
    A model representing user tokens for authentication.

    Attributes:
        user (ForeignKey): The user associated with the token.
        Access_token (CharField): The access token.
        Refresh_token (CharField): The refresh token.
        User_agent (CharField): The user agent of the device used for authentication.
        Ip_address (GenericIPAddressField): The IP address of the device.
        Platform (CharField): The platform used for authentication.
    :param user: The user associated with the token.
    :param access_token: The access token.
    :param refresh_token: The refresh token.
    :param user_agent: The user agent of the device used for authentication.
    :param ip_address: The IP address of the device.
    :param platform: The platform used for authentication.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    access_token = models.CharField(max_length=255)
    refresh_token = models.CharField(max_length=255)
    user_agent = models.CharField(max_length=255)
    ip_address = models.GenericIPAddressField()
    platform = models.CharField(max_length=255)

    def __str__(self) -> str:
        """
        Returns a string representation of the token (user and platform).
        """
        return f"Token for {self.ip_address} on {self.platform}"


class CacheToken(models.Model):
    """
    A model representing cached tokens for users.

    Attributes:
        user (ForeignKey): The user associated with the cached token.
        Token_key (PositiveIntegerField): A unique key for the token.
        Access_token (TextField): The cached access token.
    :param user: The user associated with the cached token.
    :param token_key: A unique key for the token.
    :param access_token: The cached access token.
    """

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token_key = models.PositiveIntegerField(unique=True)
    access_token = models.TextField()

    def __str__(self) -> str:
        """
        Returns a string representation of the cached token (token key).
        """
        return f"Cache Entry - {self.token_key}"
