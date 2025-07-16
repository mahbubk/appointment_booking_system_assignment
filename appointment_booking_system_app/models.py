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


class Division(Time):
    """Represents a top-level administrative division (e.g., a state or province)."""

    name = models.TextField()

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.name)


class District(Time):
    """Represents a subdivision within a Division."""

    name = models.TextField()
    division = models.ForeignKey(
        Division, on_delete=models.SET_NULL, null=True, blank=True
    )

    # pylint: disable=too-few-public-methods
    class Meta:
        """division with district"""

        unique_together = ("division", "name")

    def __str__(self):
        return f"{self.name}, {self.division}"


class Thana(Time):
    """Represents a police precinct within a District."""

    name = models.TextField()
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, blank=True
    )

    # pylint: disable=too-few-public-methods
    class Meta:
        """District with thana"""

        unique_together = ("district", "name")

    def __str__(self):
        return f"{self.name}, {self.district}"


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

    fullname = models.TextField()
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
    license_number = models.CharField(max_length=50, unique=True, null=True, blank=True)
    experience_years = models.CharField(blank=True, null=True)
    consultation_fee = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.00
    )
    is_active = models.BooleanField(
        default=True
    )  # True for active user and False for inactive user

    def __str__(self):
        """Return a human-readable string representation of the model instance."""
        return str(self.fullname)


class Specialization(Time):
    """Doctor Specialization"""

    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """Specialization  Name"""

        ordering = ["name"]

    def __str__(self):
        return str(self.name)


class DoctorProfile(Time):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
    )
    specialization = models.ForeignKey(
        Specialization, on_delete=models.SET_NULL, null=True, blank=True
    )
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"Dr. {self.user.fullname}"


class TimeSlot(Time):
    WEEKDAY_CHOICES = [
        (0, "Friday"),
        (1, "Saturday"),
        (2, "Sunday"),
        (3, "Monday"),
        (4, "Wednesday"),
        (5, "Thursday"),
        (6, "Sunday"),
    ]

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        unique_together = ["doctor", "weekday", "start_time", "end_time"]
        ordering = ["weekday", "start_time"]


class Appointment(Time):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("confirmed", "Confirmed"),
        ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]

    patient = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    doctor = models.ForeignKey(
        DoctorProfile,
        on_delete=models.CASCADE,
    )
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    notes = models.TextField(blank=True, help_text="Symptoms or notes")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")

    consultation_fee = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )

    class Meta:
        ordering = ["-appointment_date", "-appointment_time"]
        unique_together = ["doctor", "appointment_date", "appointment_time"]

    def __str__(self):
        return (
            f"{self.patient.fullname} -> Dr. {self.doctor.user.fullname} "
            f"on {self.appointment_date}"
        )


class AppointmentStatusLog(Time):
    """Track appointment status changes"""

    appointment = models.ForeignKey(
        Appointment,
        on_delete=models.CASCADE,
    )
    previous_status = models.CharField(max_length=10, blank=True)
    new_status = models.CharField(max_length=10)
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reason = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.appointment.booking_reference}: {self.previous_status} -> {self.new_status}"

    class Meta:
        ordering = ["-timestamp"]


class MonthlyReport(Time):
    """Monthly reports for doctors"""

    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    year = models.IntegerField()
    month = models.IntegerField()
    total_appointments = models.IntegerField(default=0)
    total_patients = models.IntegerField(default=0)
    total_earnings = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def __str__(self):
        return f"Dr. {self.doctor.user.fullname} - {self.year}-{self.month:02d}"

    class Meta:
        unique_together = ["doctor", "year", "month"]
        ordering = ["-year", "-month"]


class AppointmentReminder(models.Model):
    """Track appointment reminders"""

    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    reminder_type = models.CharField(max_length=20, default="24_hours")
    sent_at = models.DateTimeField(auto_now_add=True)
    is_sent = models.BooleanField(default=False)

    class Meta:
        unique_together = ["appointment", "reminder_type"]


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
