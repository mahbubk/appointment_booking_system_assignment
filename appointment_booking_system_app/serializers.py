"""Serializers for an appointment booking system."""
from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.utils import timezone
from rest_framework import serializers

from appointment_booking_system_app.models import (
    District,
    Division,
    DoctorProfile,
    Specialization,
    Thana,
    User,
    TimeSlot,
)
from utils.api_utils import ApiUtils
from utils.utils import validate_image_file, validate_password_strength
from .models import Appointment


class DivisionSerializer(serializers.ModelSerializer):
    """
    API view to retrieve a list of all divisions.

    This view handles GET requests and returns a serialized list of all
    Division model instances in the system.
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Handle GET request to retrieve all division records.

        Returns:
            Response: A JSON response containing serialized division data.
        """

        model = Division
        fields = "__all__"


class DistrictSerializer(serializers.ModelSerializer):
    """
    API view to retrieve a list of all divisions.

    This view handles GET requests and returns a serialized list of all
    District model instances in the system.
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Handle GET request to retrieve all district records.

        Returns:
            Response: A JSON response containing serialized district data.
        """

        model = District
        fields = "__all__"


class ThanaSerializer(serializers.ModelSerializer):
    """
    API view to retrieve a list of all Thana.

    This view handles GET requests and returns a serialized list of all
    Thana model instances in the system.
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Handle GET request to retrieve all Thana records.

        Returns:
            Response: A JSON response containing serialized Thana data.
        """

        model = Thana
        fields = "__all__"


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model with role-specific validation and custom field processing.
    """

    profile_picture = serializers.ImageField(required=False, allow_null=True)
    password = serializers.CharField(write_only=True, required=True)
    phone = serializers.CharField(required=True)

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Handle GET request to retrieve all User records.

        Returns:
            Response: A JSON response containing serialized Thana data.
        """

        model = User
        fields = "__all__"

    def validate(self, attrs):
        """
        Custom validation logic for UserSerializer.
        - Checks if DOCTOR has all required fields.
        - Validates password strength.
        - Validates profile picture.
        - Formats phone number.
        """
        attrs = super().validate(attrs)

        user_type = attrs.get("user_type")

        attrs["is_active"] = True

        if user_type == "DOCTOR":
            required_fields = [
                "license_number",
                "experience_years",
                "consultation_fee",
            ]
            errors = {
                field: f"{field.replace('_', ' ').title()} is required for doctors."
                for field in required_fields
                if not attrs.get(field)
            }
            if errors:
                raise serializers.ValidationError(errors)

        attrs.get("password")
        if "password" in attrs:
            password_errors = validate_password_strength(attrs["password"])
            if password_errors:
                raise serializers.ValidationError({"password": password_errors})

        if "phone" in attrs:
            attrs["phone"] = ApiUtils.format_mobile_number(attrs["phone"])

        return attrs

    def create(self, validated_data):
        """
        Custom create method to handle profile picture and password hashing.
        """
        profile_picture = validated_data.pop("profile_picture", None)

        password = validated_data.pop("password")
        validated_data["password"] = make_password(password)

        user = super().create(validated_data)

        if profile_picture:
            try:
                user.profile_picture = validate_image_file(profile_picture)
                user.save()
            except ValidationError as e:
                raise serializers.ValidationError({"profile_picture": str(e)})

        return user

    def update(self, instance, validated_data):
        """
        Custom update method to handle profile picture and password hashing.
        """
        profile_picture = validated_data.pop("profile_picture", None)

        if "password" in validated_data:
            validated_data["password"] = make_password(validated_data["password"])

        user = super().update(instance, validated_data)

        if profile_picture is not None:
            try:
                if profile_picture:
                    user.profile_picture = validate_image_file(profile_picture)
                else:
                    user.profile_picture = None
                user.save()
            except ValidationError as e:
                raise serializers.ValidationError({"profile_picture": str(e)})

        return user


# pylint: disable=abstract-method
class UserLoginSerializer(serializers.Serializer):
    """
    serializer class for user login data.

    this serializer is used to validate and deserialize user login data,
    including the email and password fields.

    Attributes:
        email (serializers.CharField):
        A field for the user's username or email or phone.
        password (serializers.CharField): A field for the user's password (write-only).

    """

    email = serializers.CharField()
    password = serializers.CharField(write_only=True)


class SpecializationSerializer(serializers.ModelSerializer):
    """
    Serializer for the Specialization model.
    """

    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass for SpecializationSerializer.
        """

        model = Specialization
        fields = "__all__"


class DoctorProfileSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta:
        """
        Metaclass for DoctorProfileSerializer.
        """

        model = DoctorProfile
        fields = "__all__"

    def validate(self, attrs):
        user = attrs.get("user")
        if self.instance and "user" not in attrs:
            user = self.instance.user
        if user and user.user_type != "DOCTOR":
            raise serializers.ValidationError(
                {"user": "Associated user must be type of DOCTOR"}
            )
        return attrs

    def create(self, validated_data):
        user = validated_data["user"]
        if user.user_type != "DOCTOR":
            raise serializers.ValidationError(
                {"user": "User must be a DOCTOR to create a doctor profile"}
            )
        return super().create(validated_data)


class TimeSlotSerializer(serializers.ModelSerializer):
    # pylint: disable=too-few-public-methods
    class Meta:
        model = TimeSlot
        fields = "__all__"
        extra_kwargs = {
            "doctor": {"required": True},
            "weekday": {"required": True},
            "start_time": {"required": True},
            "end_time": {"required": True},
        }

    def validate(self, attrs):
        """
        Validate that start time is before end time and check for overlapping slots
        """
        # Check time order
        if attrs["start_time"] >= attrs["end_time"]:
            raise serializers.ValidationError(
                {"time": "Start time must be before end time"}
            )

        # Check for overlapping time slots for the same doctor on the same weekday
        overlapping_slots = TimeSlot.objects.filter(
            doctor=attrs["doctor"],
            weekday=attrs["weekday"],
            start_time__lt=attrs["end_time"],
            end_time__gt=attrs["start_time"],
        )

        # Exclude current instance when updating
        if self.instance:
            overlapping_slots = overlapping_slots.exclude(pk=self.instance.pk)

        if overlapping_slots.exists():
            raise serializers.ValidationError(
                {"time": "This time slot overlaps with an existing slot"}
            )

        return attrs

    @staticmethod
    def validate_weekday(value):
        """Validate weekday is within allowed choices"""
        if value not in dict(TimeSlot.WEEKDAY_CHOICES).keys():
            raise serializers.ValidationError("Invalid weekday selection")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    patient = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.filter(user_type="patient"),
        required=True,  # pylint: disable=no-member
    )
    doctor = serializers.PrimaryKeyRelatedField(
        queryset=DoctorProfile.objects.all(), required=True  # pylint: disable=no-member
    )

    # pylint: disable=too-few-public-methods
    class Meta:
        model = Appointment
        fields = "__all__"
        read_only_fields = [
            "status",
            "consultation_fee",
        ]

    @staticmethod
    def validate_appointment_date(value):
        """Validate appointment date is in the future"""
        if value < timezone.now().date():
            raise serializers.ValidationError("Appointment date cannot be in the past.")
        return value

    @staticmethod
    def validate_appointment_time(value):
        """Basic time validation (could add business hours check)"""
        if (
            value < datetime.strptime("09:00", "%H:%M").time()
            or value > datetime.strptime("17:00", "%H:%M").time()
        ):
            raise serializers.ValidationError(
                "Appointments must be between 9AM and 5PM"
            )
        return value

    def validate(self, attrs):
        """Cross-field validation"""
        appointment_datetime = timezone.make_aware(
            datetime.combine(attrs["appointment_date"], attrs["appointment_time"])
        )

        if appointment_datetime <= timezone.now():
            raise serializers.ValidationError(
                "Appointment cannot be scheduled in the past."
            )

        doctor = attrs["doctor"]
        weekday = attrs["appointment_date"].weekday()
        available_slots = doctor.time_slots.filter(
            weekday=weekday,
            start_time__lte=attrs["appointment_time"],
            end_time__gt=attrs["appointment_time"],
            is_active=True,
        )

        if not available_slots.exists():
            raise serializers.ValidationError("Doctor is not available at this time.")

        conflicting_appointments = (
            Appointment.objects.filter(  # pylint: disable=no-member
                doctor=doctor,
                appointment_date=attrs["appointment_date"],
                appointment_time=attrs["appointment_time"],
                status__in=["pending", "confirmed"],
            ).exclude(pk=self.instance.pk if self.instance else None)
        )

        if conflicting_appointments.exists():
            raise serializers.ValidationError("This time slot is already booked.")

        return attrs

    def create(self, validated_data):
        """Handle creation with auto fields"""

        validated_data["status"] = "pending"

        if "consultation_fee" not in validated_data:
            validated_data["consultation_fee"] = validated_data[
                "doctor"
            ].consultation_fee

        appointment = super().create(validated_data)

        appointment.save()

        return appointment

    def update(self, instance, validated_data):
        """Prevent updating certain fields if appointment is completed/canceled"""
        if instance.status in ["completed", "cancelled"]:
            raise serializers.ValidationError(
                "Cannot modify completed or cancelled appointments."
            )

        return super().update(instance, validated_data)
