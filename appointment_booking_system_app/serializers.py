"""Serializers for appointment booking system."""


from rest_framework import serializers

from appointment_booking_system_app.models import District, Division, Thana, User


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
    Serializer for the User model with role-specific validation.
    - Raises validation errors if DOCTOR is missing required fields.
    """
    # profile_picture = serializers.ImageField(required=False, allow_null=True)
    full_name = serializers.CharField(source="full_name", read_only=True)


    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            'password': {'write_only': True}  # Never return password in responses
        }

    def validate_password(self, value):
        """
        Validate password strength before hashing
        """
        errors = []

        if len(value) < 8:
            errors.append("Password must be at least 8 characters long.")

        if not any(char.isupper() for char in value):
            errors.append("Password must contain at least one uppercase letter.")

        if not any(char.isdigit() for char in value):
            errors.append("Password must contain at least one digit.")

        if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in value):
            errors.append("Password must contain at least one special character.")

        if errors:
            raise serializers.ValidationError(errors)

        return value

    def validate(self, attrs):
        """
        Custom validation logic for UserSerializer.
        - Checks if DOCTOR has all required fields.
        """
        user_type = attrs.get("user_type")
        is_active = attrs.get("is_active", True)  # Default to True if not provided

        if user_type == "DOCTOR" and is_active:
            required_fields = [
                "license_number",
                "total_experience",
                "consultation_fee",
                "availability",
            ]
            errors = {}

            for field in required_fields:
                if not attrs.get(field):
                    errors[field] = f"{field.replace('_', ' ').title()} is required for doctors."

            if errors:
                raise serializers.ValidationError(errors)

        return attrs
