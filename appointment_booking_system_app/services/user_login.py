""" User Login Authenticator Utils"""
from django.core.exceptions import ObjectDoesNotExist

from appointment_booking_system_app.models import User
from appointment_booking_system_app.services.authentication import Authentication


def authenticate_user(email, password):
    """
    Authenticate user using username, email, or phone number with ISD code.

    Args:
        email (str): The username, email, or phone number of the user.
        password (str): The user's password.


    Returns:
        tuple: (User instance, error_message) or (None, error_message)
    """
    try:
        user = User.objects.filter(email=email).first()  # pylint: disable=no-member

        if user is None:
            error_message = "User not registered."
            return None, error_message

        if not Authentication.verify_password(user.password, password):
            error_message = "Invalid credentials."
            return None, error_message

        if not user.is_active:
            error_message = "User account is inactive."
            return None, error_message

        return user, None

    except ObjectDoesNotExist:
        error_message = "An error occurred during authentication."
        return None, error_message
