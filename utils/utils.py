"""
Provides Utilities functions for encoding and decoding  data and others

"""
import os

from rest_framework.exceptions import ValidationError as DRFValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile, TemporaryUploadedFile
from rest_framework.exceptions import ValidationError

def validate_password_strength(password) -> None:
    """
    Validate the strength of a password.

    Args:
        password (str): The password to validate.

    Raises:
        DRFValidationError: If the password does not meet the strength requirements.
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

    if errors:
        raise DRFValidationError(errors)


# def validate_image_file(file_path: str) -> str:
#     """
#     Validates an image file to ensure it meets the following criteria:
#     - File is either JPEG or PNG (based on MIME type or extension)
#     - File size does not exceed 5 MB
#
#     Args:
#         file_path (str): Path to the file to be validated.
#
#     Returns:
#         dict:
#             - If valid: {"status": "success", "file": file_path}
#             - If invalid: {"status": "error", "message": "Error description"}
#     """
#
#     errors = []
#
#     if not os.path.exists(file_path):
#         errors.append("File does not exist.")
#
#     # Calculate file size (5 MB = 5 * 1024 * 1024 bytes)
#     max_size = 5 * 1024 * 1024  # 5 MB in bytes
#     file_size = os.path.getsize(file_path)
#
#     if file_size > max_size:
#         errors.append("File size exceeds 5 MB limit.")
#
#     allowed_extensions = {".jpg", ".jpeg", ".png"}
#     file_extension = os.path.splitext(file_path)[1].lower()
#
#     if file_extension not in allowed_extensions:
#         errors.append(f"File extension must be one of {allowed_extensions}")
#
#     if errors:
#         raise DRFValidationError(errors)
#     return file_path


def validate_image_file(uploaded_file):
    """
    Validate an uploaded image file (handles both single file and list cases)
    """
    # Handle case where file comes as a list
    if isinstance(uploaded_file, list):
        if len(uploaded_file) > 1:
            raise ValidationError("Only one profile picture allowed")
        uploaded_file = uploaded_file[0]

    # Now validate the single file
    max_size = 5 * 1024 * 1024  # 5MB
    if uploaded_file.size > max_size:
        raise ValidationError("File size exceeds 5 MB limit")

    valid_content_types = ['image/jpeg', 'image/png']
    if uploaded_file.content_type not in valid_content_types:
        raise ValidationError("Only JPEG and PNG images are allowed")

    valid_extensions = ['.jpg', '.jpeg', '.png']
    file_name = uploaded_file.name.lower()
    if not any(file_name.endswith(ext) for ext in valid_extensions):
        raise ValidationError(f"Invalid file extension. Allowed: {', '.join(valid_extensions)}")
