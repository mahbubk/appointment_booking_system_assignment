# pylint: disable=too-many-lines
""" Views """
import jwt
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response

from utils.api_utils import ApiUtils
from utils.exception_handler import handle_exceptions
from utils.responses import Responses
from utils.strings import ResponseMessages
from .db_cache import DbCache
from .models import (
    Appointment,
    District,
    Division,
    Specialization,
    Thana,
    TimeSlot,
    Token,
    AppointmentReminder,
    MonthlyReport,
)
from .repository.doctor_profile import doctor_profile_service
from .repository.user import user_service
from .serializers import (
    AppointmentSerializer,
    DistrictSerializer,
    DivisionSerializer,
    DoctorProfileSerializer,
    SpecializationSerializer,
    ThanaSerializer,
    TimeSlotSerializer,
    UserLoginSerializer,
    UserSerializer,
    AppointmentReminderSerializer,
    MonthlyReportSerializer,
)
from .services.authentication import Authentication
from .services.custom_jwt_authentication import AllowAnyCustom, CustomJWTAuthentication
from .services.user_login import authenticate_user

db_cache = DbCache()
auth = Authentication()


class DivisionViewSet(viewsets.ViewSet):
    """
    A view set for handling CRUD operations on Division instances.
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        Retrieve a list of all Division instances.

        Returns:
            Response: A response containing serialized Division instances.
        """
        divisions = Division.objects.all()  # pylint: disable=no-member

        serializer = DivisionSerializer(divisions, many=True)  # type: ignore
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def create(request) -> Response:
        """
        Create a new Division instance.

        Args:
            request: The HTTP request containing data for the new instance.

        Returns:
            Response: A response containing serialized data of the created Division instance.
        """
        serializer = DivisionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        retrieve details of a specific Division instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the Division instance to retrieve.

        Returns:
            Response: A response containing serialized
            data of the requested Division instance.
        """
        division_obj = Division.objects.get(pk=pk)  # pylint: disable=no-member

        if not division_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DivisionSerializer(division_obj)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def partial_update(request, pk: int) -> Response:
        """
        partially update details of a specific Division instance.

        Args:
            request: The HTTP request containing partially updated data.
            pk (int): The primary key of the Division instance to partially update.

        Returns:
            Response: A response containing serialized
            data of the partially updated Division instance.
        """
        division_obj = Division.objects.get(pk=pk)  # pylint: disable=no-member

        if not division_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DivisionSerializer(division_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific Division instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the Division instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        division_obj = Division.objects.get(pk=pk)  # pylint: disable=no-member

        if not division_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        Division.objects.get(pk=pk).delete()  # pylint: disable=no-member
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


class DistrictViewSet(viewsets.ViewSet):
    """
    A view set for handling CRUD operations on District instances.
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        Retrieve a list of all District instances.

        Returns:
            Response: A response containing serialized District instances.
        """
        districts = District.objects.all()  # pylint: disable=no-member

        serializer = DistrictSerializer(districts, many=True)  # type: ignore
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def create(request) -> Response:
        """
        Create a new District instance.

        Args:
            request: The HTTP request containing data for the new instance.

        Returns:
            Response: A response containing serialized data of the created District instance.
        """
        serializer = DistrictSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        retrieve details of a specific District instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the District instance to retrieve.

        Returns:
            Response: A response containing serialized
            data of the requested District instance.
        """
        district_obj = District.objects.get(pk=pk)  # pylint: disable=no-member

        if not district_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DivisionSerializer(district_obj)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def partial_update(request, pk: int) -> Response:
        """
        partially update details of a specific District instance.

        Args:
            request: The HTTP request containing partially updated data.
            pk (int): The primary key of the District instance to partially update.

        Returns:
            Response: A response containing serialized
            data of the partially updated District instance.
        """
        district_obj = District.objects.get(pk=pk)  # pylint: disable=no-member

        if not district_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DivisionSerializer(district_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific District instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the District instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        district_obj = District.objects.get(pk=pk)  # pylint: disable=no-member

        if not district_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        District.objects.get(pk=pk).delete()  # pylint: disable=no-member
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


class ThanaViewSet(viewsets.ViewSet):
    """
    A view set for handling CRUD operations on Thana instances.
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        Retrieve a list of all Thana instances.

        Returns:
            Response: A response containing serialized Thana instances.
        """
        thanas = Thana.objects.all()  # pylint: disable=no-member

        serializer = ThanaSerializer(thanas, many=True)  # type: ignore
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def create(request) -> Response:
        """
        Create a new Thana instance.

        Args:
            request: The HTTP request containing data for the new instance.

        Returns:
            Response: A response containing serialized data of the created Thana instance.
        """
        serializer = ThanaSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        retrieve details of a specific Thana instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the Thana instance to retrieve.

        Returns:
            Response: A response containing serialized
            data of the requested Thana instance.
        """
        thana_obj = Thana.objects.get(pk=pk)  # pylint: disable=no-member

        if not thana_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DivisionSerializer(thana_obj)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def partial_update(request, pk: int) -> Response:
        """
        partially update details of a specific Thana instance.

        Args:
            request: The HTTP request containing partially updated data.
            pk (int): The primary key of the Thana instance to partially update.

        Returns:
            Response: A response containing serialized
            data of the partially updated Thana instance.
        """
        thana_obj = Thana.objects.get(pk=pk)  # pylint: disable=no-member

        if not thana_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DivisionSerializer(thana_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific Thana instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the Thana instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        thana_obj = Thana.objects.get(pk=pk)  # pylint: disable=no-member

        if not thana_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        Thana.objects.get(pk=pk).delete()  # pylint: disable=no-member
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


class UserViewSet(viewsets.ViewSet):
    """
    A view set for handling CRUD operations on User instances.
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        retrieve a list of all InternalUser instances.

        Returns:
            Response: A response containing serialized InternalUser instances.
        """
        users_list = user_service.get_all()
        serializer = UserSerializer(users_list, many=True)
        if not users_list:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    # After user creation, you can uncomment the below line
    # @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def create(request) -> Response:
        """
        Create a new User Instance.

        """
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=Responses.error_response(message=serializer.errors),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = serializer.save()

        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                data=UserSerializer(user).data,
            ),
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        retrieve details of a specific User instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the InternalUser instance to retrieve.

        Returns:
            Response: A response containing serialized data of the requested InternalUser instance.
        """

        user = user_service.get_by_id(pk=pk)
        if not user:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                data=UserSerializer(user).data,
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def partial_update(request, pk: int) -> Response:
        """
        partially update details of a
        specific User instance.
        Args:
            request: The HTTP request containing partially updated data.
            pk (int): The primary key of the User
            instance to partially update.
        Returns:
            Response: A response containing serialized data
            of the partially updated User instance.
        """
        user = user_service.get_by_id(pk=pk)
        if not user:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            updated_user = user_service.partial_update(user, serializer.validated_data)
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=UserSerializer(updated_user).data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific User instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the User instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        user = user_service.get_by_id(pk=pk)

        if not user:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        user_service.delete(user)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


class UserSessionManagementViewSet(viewsets.ViewSet):
    """
    A ViewSet for managing user session operations such as login and logout.

    This class handles user authentication by validating credentials and generating
    JWT tokens upon successful login. It also provides functionality to invalidate
    access tokens during logout, ensuring secure session termination.

    Methods:
        login(request): Authenticates a user using username/email/phone and password,
                        and return access and refresh tokens.
        Logout(request): Invalidates the user's access token, effectively logging the user out.
    """

    @staticmethod
    @AllowAnyCustom.allow_any
    def login(request):
        """
        Handle user login and token generation.

        Args:
            request: The HTTP request.

        Returns:
            Response: The response containing login results and tokens.
        """
        serializer = UserLoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(
                data=Responses.error_response(message=serializer.errors),
                status=status.HTTP_400_BAD_REQUEST,
            )

        email = serializer.validated_data["email"]
        password = serializer.validated_data["password"]
        fingerprint = auth.get_browser_fingerprint(request)

        user, error_message = authenticate_user(
            email=email,
            password=password,
        )

        if user is None:
            return Response(
                data=Responses.error_response(message=error_message),
                status=status.HTTP_401_UNAUTHORIZED,
            )

        if not user.is_active:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.INACTIVE_USER.value
                ),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user.last_login_date = timezone.now()
        user.save()

        access_token, refresh_token = ApiUtils.generate_and_store_tokens(
            user, fingerprint
        )

        return Response(
            data=Responses.success_response(
                message="Login successful!",
                data={"access_token": access_token, "refresh_token": refresh_token},
            ),
            status=status.HTTP_201_CREATED,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    def logout(request):
        """
        Invalidate the user's access token to handle the logout operation.

        Args:
            request (HttpRequest): The HTTP request object.

        Returns:
            Response: A response indicating the success
            or failure of the logout operation.
        """

        token = request.headers.get("Api-Key")

        if not token:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.TOKEN_MISSING.value
                ),
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            token = Token.objects.get(access_token=token)  # pylint: disable=no-member
            db_cache.delete_token(user_id=token.user_id)
            return Response(
                data=Responses.success_response(message="Logout successful!"),
                status=status.HTTP_200_OK,
            )

        except jwt.exceptions.ExpiredSignatureError:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.TOKEN_EXPIRED.value
                ),
                status=status.HTTP_401_UNAUTHORIZED,
            )
        except jwt.exceptions.DecodeError:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.TOKEN_INVALID.value
                ),
                status=status.HTTP_401_UNAUTHORIZED,
            )


class AccessTokenFromRefreshToken(viewsets.ViewSet):
    """View for generating a new access token from a refresh token."""

    @staticmethod
    @handle_exceptions
    def create(request):
        """
        generate a new access token from a refresh token.

        Args:
            request: The HTTP request.
        Returns:
            Response: The response containing
            the new access token or an error message.
        """
        fingerprint = auth.get_browser_fingerprint(request)

        refresh_token = request.headers.get("Refresh-Token")
        refresh_token_exists, expired = ApiUtils.is_refresh_token_expired(refresh_token)
        if expired or refresh_token_exists is False:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.REFRESH_TOKEN_EXPIRED.value
                ),
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            (
                new_access_token,
                new_refresh_token,
            ) = auth.create_access_token_from_refresh_token(refresh_token, fingerprint)
            data = {
                "refresh_token": new_refresh_token,
                "access_token": new_access_token,
            }
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=data
                ),
                status=status.HTTP_201_CREATED,
            )
        except ValueError as exe:
            return Response(
                data=Responses.error_response(message=str(exe)),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )


class SpecializationViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling CRUD Specialization operations.
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        Retrieve a list of all Specialization instances.

        Returns:
            Response: A response containing serialized Specialization instances.
        """
        specializations = Specialization.objects.all()  # pylint: disable=no-member

        serializer = SpecializationSerializer(specializations, many=True)  # type: ignore
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def create(request) -> Response:
        """
        Create a new instance.

        Args:
            request: The HTTP request containing data for the new instance.

        Returns:
            Response: A response containing serialized data of the created instance.
        """
        serializer = SpecializationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        retrieve details of a specific instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the instance to retrieve.

        Returns:
            Response: A response containing serialized
            data of the requested instance.
        """
        specialization_obj = Specialization.objects.get(
            pk=pk
        )  # pylint: disable=no-member

        if not specialization_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SpecializationSerializer(specialization_obj)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def partial_update(request, pk: int) -> Response:
        """
        partially update details of a specific instance.

        Args:
            request: The HTTP request containing partially updated data.
            pk (int): The primary key of the instance to partially update.

        Returns:
            Response: A response containing serialized
            data of the partially updated instance.
        """
        specialization_obj = Specialization.objects.get(
            pk=pk
        )  # pylint: disable=no-member

        if not specialization_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = SpecializationSerializer(
            specialization_obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        specialization_obj = Specialization.objects.get(
            pk=pk
        )  # pylint: disable=no-member

        if not specialization_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        Specialization.objects.get(pk=pk).delete()  # pylint: disable=no-member
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


class DoctorProfileViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling CRUD DoctorProfile operations and
    Filter doctors by specialization, availability, and location.
    And Filter appointments by date range, status, and doctor
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        Retrieve a list of all Specialization instances.

        Returns:
            Response: A response containing serialized Specialization instances.
        """
        doctor_profiles = doctor_profile_service.get_all()

        serializer = DoctorProfileSerializer(doctor_profiles, many=True)  # type: ignore
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def create(request) -> Response:
        """
        Create a new instance.

        Args:
            request: The HTTP request containing data for the new instance.

        Returns:
            Response: A response containing serialized data of the created instance.
        """
        serializer = DoctorProfileSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        retrieve details of a specific instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the instance to retrieve.

        Returns:
            Response: A response containing serialized
            data of the requested instance.
        """
        doctor_profile_obj = doctor_profile_service.get_by_id(pk=pk)

        if not doctor_profile_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DoctorProfileSerializer(doctor_profile_obj)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def partial_update(request, pk: int) -> Response:
        """
        partially update details of a specific instance.

        Args:
            request: The HTTP request containing partially updated data.
            pk (int): The primary key of the instance to partially update.

        Returns:
            Response: A response containing serialized
            data of the partially updated instance.
        """
        doctor_profile_obj = doctor_profile_service.get_by_id(pk=pk)

        if not doctor_profile_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = DoctorProfileSerializer(
            doctor_profile_obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        doctor_profile_obj = doctor_profile_service.get_by_id(pk=pk)

        if not doctor_profile_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        doctor_profile_service.delete(doctor_profile_obj)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def filter_doctors(request) -> Response:  # pylint: disable=unused-argument
        """
        Filter and retrieve a list of doctor profiles based on optional query parameters.

        Supported query parameters:
            - division_id (int): ID of the division where the doctor is located.
            - district_id (int): ID of the district where the doctor is located.
            - thana_id (int): ID of the thana where the doctor is located.
            - specialization_id (int): ID of the doctor's specialization.

        Returns:
            Response: A JSON response containing either:
                - A success message with a list of matching doctor profiles (as dictionaries).
                - A 404 error response if no doctors are found.
        """
        query_params = request.query_params.dict()
        doctor_profile_obj = doctor_profile_service.get_filter_doctors(query_params)

        if not doctor_profile_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                data=doctor_profile_obj,
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def filtered_appointments(request) -> Response:  # pylint: disable=unused-argument
        """
        Filter and retrieve a list of doctor profiles based on optional query parameters.

        Supported query parameters:
            - division_id (int): ID of the division where the doctor is located.
            - district_id (int): ID of the district where the doctor is located.
            - thana_id (int): ID of the thana where the doctor is located.
            - specialization_id (int): ID of the doctor's specialization.

        Returns:
            Response: A JSON response containing either:
                - A success message with a list of matching doctor profiles (as dictionaries).
                - A 404 error response if no doctors are found.
        """
        query_params = request.query_params.dict()
        appointment_obj = doctor_profile_service.get_filtered_appointments(query_params)

        if not appointment_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                data=appointment_obj,
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def user_specific_appointments(request):
        user, _ = CustomJWTAuthentication().authenticate(request)

        appointments = doctor_profile_service.get_user_specific_appointments(user)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                data=appointments,
            ),
            status=status.HTTP_200_OK,
        )


class TimeSlotViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling CRUD TimeSlot operations for Doctors.
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        Retrieve a list of all instances.

        Returns:
            Response: A response containing serialized instances.
        """
        timeslots = TimeSlot.objects.all()  # pylint: disable=no-member

        serializer = TimeSlotSerializer(timeslots, many=True)  # type: ignore
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def create(request) -> Response:
        """
        Create a new instance.

        Args:
            request: The HTTP request containing data for the new instance.

        Returns:
            Response: A response containing serialized data of the created instance.
        """
        serializer = TimeSlotSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        retrieve details of a specific instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the instance to retrieve.

        Returns:
            Response: A response containing serialized
            data of the requested instance.
        """
        time_slot_obj = TimeSlot.objects.get(pk=pk)  # pylint: disable=no-member

        if not time_slot_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TimeSlotSerializer(time_slot_obj)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def partial_update(request, pk: int) -> Response:
        """
        partially update details of a specific instance.

        Args:
            request: The HTTP request containing partially updated data.
            pk (int): The primary key of the instance to partially update.

        Returns:
            Response: A response containing serialized
            data of the partially updated instance.
        """
        time_slot_obj = TimeSlot.objects.get(pk=pk)  # pylint: disable=no-member

        if not time_slot_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = TimeSlotSerializer(time_slot_obj, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        time_slot_obj = TimeSlot.objects.get(pk=pk)  # pylint: disable=no-member

        if not time_slot_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        TimeSlot.objects.get(pk=pk).delete()  # pylint: disable=no-member
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


class AppointmentViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling CRUD Appointments.
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        Retrieve a list of all instances.

        Returns:
            Response: A response containing serialized instances.
        """
        appointments = Appointment.objects.all()  # pylint: disable=no-member

        serializer = AppointmentSerializer(appointments, many=True)  # type: ignore
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def create(request) -> Response:
        """
        Create a new instance.

        Args:
            request: The HTTP request containing data for the new instance.

        Returns:
            Response: A response containing serialized data of the created instance.
        """
        serializer = AppointmentSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_201_CREATED,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_422_UNPROCESSABLE_ENTITY,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        retrieve details of a specific instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the instance to retrieve.

        Returns:
            Response: A response containing serialized
            data of the requested instance.
        """
        appointment_obj = Appointment.objects.get(pk=pk)  # pylint: disable=no-member

        if not appointment_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AppointmentSerializer(appointment_obj)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def partial_update(request, pk: int) -> Response:
        """
        partially update details of a specific instance.

        Args:
            request: The HTTP request containing partially updated data.
            pk (int): The primary key of the instance to partially update.

        Returns:
            Response: A response containing serialized
            data of the partially updated instance.
        """
        appointment_obj = Appointment.objects.get(pk=pk)  # pylint: disable=no-member

        if not appointment_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = AppointmentSerializer(
            appointment_obj, data=request.data, partial=True
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                data=Responses.success_response(
                    message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                    data=serializer.data,
                ),
                status=status.HTTP_200_OK,
            )
        return Response(
            data=Responses.error_response(message=serializer.errors),
            status=status.HTTP_400_BAD_REQUEST,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        appointment_obj = Appointment.objects.get(pk=pk)  # pylint: disable=no-member

        if not appointment_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        Appointment.objects.get(pk=pk).delete()  # pylint: disable=no-member
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


class AppointmentReportViewSet(viewsets.ViewSet):
    """
    A ViewSet for handling reminder, reporting and analytics related to appointments.

    This ViewSet provides endpoints to:
    - Retrieve appointment reminders sent to patients.
    - Fetch monthly performance reports per doctor, including total appointments,
      unique patients, and total earnings.

    Authentication:
        Requires JWT-based authentication.

    Endpoints:
        - GET /api/v1/appointments/reminders/
        - GET /api/v1/appointments/monthly-reports/

    Query Parameters (optional):
        For reminders:
            - appointment_id: Filter reminders by specific appointment.
            - date: Filter reminders by sent date (YYYY-MM-DD).

        For monthly reports:
            - doctor_id: Filter reports for a specific doctor.
            - year: Filter by report year.
            - month: Filter by report month.

    Returns:
        Standardized JSON responses with appropriate HTTP status codes.
    """

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def appointment_reminders_list(request) -> Response:
        """
        Retrieve a list of appointment reminders.

        Query Params:
            appointment_id (optional): Filter reminders for a specific appointment.
            Date (optional): Filter reminders sent on a specific date (YYYY-MM-DD).

        Returns:
            Response: A response containing serialized appointment reminders.
        """
        reminders = AppointmentReminder.objects.all().order_by("-sent_at")

        appointment_id = request.query_params.get("appointment_id")
        if appointment_id:
            reminders = reminders.filter(appointment_id=appointment_id)

        date = request.query_params.get("date")
        if date:
            reminders = reminders.filter(sent_at__date=date)

        serializer = AppointmentReminderSerializer(reminders, many=True)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
    @CustomJWTAuthentication.jwt_authenticated
    @handle_exceptions
    def appointment_monthly_reports_list(request) -> Response:
        """
        Retrieve a list of doctor monthly reports.

        Query Params:
            doctor_id (optional): Filter by doctor.
            Year (optional): Filter by year.
            Month (optional): Filter by month.

        Returns:
            Response: A response containing serialized monthly reports.
        """
        reports = MonthlyReport.objects.all().order_by("-year", "-month")

        doctor_id = request.query_params.get("doctor_id")
        if doctor_id:
            reports = reports.filter(doctor_id=doctor_id)

        year = request.query_params.get("year")
        if year:
            reports = reports.filter(year=year)

        month = request.query_params.get("month")
        if month:
            reports = reports.filter(month=month)

        serializer = MonthlyReportSerializer(reports, many=True)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )
