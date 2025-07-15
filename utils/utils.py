"""
Provides Utilities functions for encoding and decoding  data and others

"""

from rest_framework.exceptions import ValidationError


def validate_image_file(uploaded_file):
    """
    Validate an uploaded image file (handles both single file and list cases)
    """

    if isinstance(uploaded_file, list):
        if len(uploaded_file) > 1:
            raise ValidationError("Only one profile picture allowed")
        uploaded_file = uploaded_file[0]

    max_size = 5 * 1024 * 1024  # 5MB
    if uploaded_file.size > max_size:
        raise ValidationError("File size exceeds 5 MB limit")

    valid_content_types = ["image/jpeg", "image/png"]
    if uploaded_file.content_type not in valid_content_types:
        raise ValidationError("Only JPEG and PNG images are allowed")

    valid_extensions = [".jpg", ".jpeg", ".png"]
    file_name = uploaded_file.name.lower()
    if not any(file_name.endswith(ext) for ext in valid_extensions):
        raise ValidationError(
            f"Invalid file extension. Allowed: {', '.join(valid_extensions)}"
        )

    return uploaded_file


def validate_password_strength(password) -> list[str]:
    """
    Validate the strength of a password and return a list of errors (if any).

    Args:
        password (str): The password to validate.

    Returns:
        list[str]: List of error messages (empty if password is valid).
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters long.")

    if not any(char.isupper() for char in password):
        errors.append("Password must contain at least one uppercase letter.")

    if not any(char.islower() for char in password):
        errors.append("Password must contain at least one lowercase letter.")

    if not any(char.isdigit() for char in password):
        errors.append("Password must contain at least one digit.")

    if not any(char in "!@#$%^&*()_+-=[]{}|;:,.<>?/" for char in password):
        errors.append("Password must contain at least one special character.")

    return errors
