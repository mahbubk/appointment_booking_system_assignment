"""Serializers for an appointment booking system."""
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rest_framework import serializers

from appointment_booking_system_app.models import District, Division, Thana, User
from utils.api_utils import ApiUtils
from utils.utils import validate_image_file, validate_password_strength


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
        is_active = attrs.get("is_active", True)

        if user_type == "DOCTOR" and is_active:
            required_fields = [
                "license_number",
                "total_experience",
                "consultation_fee",
                "availability",
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
