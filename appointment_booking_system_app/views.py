# pylint: disable=too-many-lines
""" Views """
import jwt
from django.utils import timezone
from rest_framework import status, viewsets
from rest_framework.response import Response

from appointment_booking_system_app.db_cache import DbCache
from appointment_booking_system_app.models import District, Division, Thana, Token
from appointment_booking_system_app.repository.user import user_service
from appointment_booking_system_app.serializers import (
    DistrictSerializer,
    DivisionSerializer,
    ThanaSerializer,
    UserLoginSerializer,
    UserSerializer,
)
from appointment_booking_system_app.services.authentication import Authentication
from appointment_booking_system_app.services.custom_jwt_authentication import (
    CustomJWTAuthentication,
)
from appointment_booking_system_app.services.user_login import authenticate_user
from utils.api_utils import ApiUtils
from utils.exception_handler import handle_exceptions
from utils.responses import Responses
from utils.strings import ResponseMessages

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
                        and returns access and refresh tokens.
        logout(request): Invalidates the user's access token, effectively logging the user out.
    """

    @staticmethod
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
