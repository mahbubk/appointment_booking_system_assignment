from django.shortcuts import render
from rest_framework import status, viewsets
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from appointment_booking_system_app.models import Division
from appointment_booking_system_app.repository.user import user_service
from appointment_booking_system_app.serializers import (
    DivisionSerializer,
    UserSerializer,
)
from utils.responses import Responses
from utils.strings import ResponseMessages

# Create your views here.


class DivisionViewSet(viewsets.ViewSet):
    """
    A view set for handling CRUD operations on Division instances.
    """

    @staticmethod
    def list(request) -> Response:  # pylint: disable=unused-argument
        """
        Retrieve a list of all Division instances.

        Returns:
            Response: A response containing serialized Division instances.
        """
        divisions = Division.objects.all()
        serializer = DivisionSerializer(divisions, many=True)
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
            ),
            status=status.HTTP_200_OK,
        )

    @staticmethod
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
        division_obj = Division.objects.get(pk=pk)

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
        division_obj = Division.objects.get(pk=pk)

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
    def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
        """
        delete it a specific Division instance.

        Args:
            request: The HTTP request.
            pk (int): The primary key of the Division instance to delete.

        Returns:
            Response: A response indicating the success of the deletion.
        """
        division_obj = Division.objects.get(pk=pk)

        if not division_obj:
            return Response(
                data=Responses.error_response(
                    message=ResponseMessages.NO_DATA_FOUND.value
                ),
                status=status.HTTP_404_NOT_FOUND,
            )

        Division.objects.get(pk=pk).delete()
        return Response(
            data=Responses.success_response(
                message=ResponseMessages.DELETE_SUCCESSFUL.value
            ),
            status=status.HTTP_204_NO_CONTENT,
        )


class UserViewSet(viewsets.ViewSet):
    """
    A view set for handling CRUD operations on InternalUser instances.
    """

    # @staticmethod
    # @CustomJWTAuthentication.jwt_authenticated
    # @ApiUtils.permission_required(feature="Users", permission="READ")
    # @handle_exceptions
    # def list(request) -> Response:
    #     """
    #     retrieve a list of all InternalUser instances.
    #
    #     Returns:
    #         Response: A response containing serialized InternalUser instances.
    #     """
    #     user, _ = CustomJWTAuthentication().authenticate(request)
    #     users_list = users_service.get_all(order_by="username", user=user)
    #     serializer = UsersSerializer(users_list, many=True)
    #     if not users_list:
    #         return Response(
    #             data=Responses.error_response(
    #                 message=ResponseMessages.NO_DATA_FOUND.value
    #             ),
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #
    #     return Response(
    #         data=Responses.success_response(
    #             message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=serializer.data
    #         ),
    #         status=status.HTTP_200_OK,
    #     )

    @staticmethod
    # @CustomJWTAuthentication.jwt_authenticated
    # @ApiUtils.permission_required(feature="Users", permission="CREATE")
    # @handle_exceptions
    def create(request) -> Response:
        """
        Create a new user and optionally assign feature permissions.

        This method creates a new user using the data provided in the request, and if feature
        permission data is provided, it associates those permissions with the created user.
        If the user permissions data is invalid, an error response with details is returned.
        Otherwise, a success response is returned with the newly created user and any associated
        permissions.

        Args:
            request: The HTTP request object containing the user data and optional feature
                    permission data.

        Returns:
            Response: A DRF Response object containing the status and either the created
                      user data or an error message.
        """
        data = request.data
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                data=Responses.error_response(message=serializer.errors),
                status=status.HTTP_422_UNPROCESSABLE_ENTITY,
            )

        user = user_service.create(data)

        return Response(
            data=Responses.success_response(
                message=ResponseMessages.REQUEST_SUCCESSFUL.value,
                data=UserSerializer(user).data,
            ),
            status=status.HTTP_201_CREATED,
        )

    # @staticmethod
    # # @CustomJWTAuthentication.jwt_authenticated
    # # @ApiUtils.permission_required(feature="Users", permission="READ")
    # # @handle_exceptions
    # def retrieve(request, pk: int) -> Response:  # pylint: disable=unused-argument
    #     """
    #     retrieve details of a specific InternalUser instance.
    #
    #     Args:
    #         request: The HTTP request.
    #         pk (int): The primary key of the InternalUser instance to retrieve.
    #
    #     Returns:
    #         Response: A response containing serialized data of the requested InternalUser instance.
    #     """
    #
    #     user = users_service.get_user_information(pk=pk)
    #     if not user:
    #         return Response(
    #             data=Responses.error_response(
    #                 message=ResponseMessages.NO_DATA_FOUND.value
    #             ),
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #     return Response(
    #         data=Responses.success_response(
    #             message=ResponseMessages.REQUEST_SUCCESSFUL.value, data=user
    #         ),
    #         status=status.HTTP_200_OK,
    #     )
    #
    # @staticmethod
    # # @CustomJWTAuthentication.jwt_authenticated
    # # @ApiUtils.permission_required(feature="Users", permission="UPDATE")
    # # @handle_exceptions
    # def partial_update(request, pk: int) -> Response:
    #     """
    #     partially update details of a
    #     specific InternalUser instance.
    #     Args:
    #         request: The HTTP request containing partially updated data.
    #         pk (int): The primary key of the InternalUser
    #         instance to partially update.
    #     Returns:
    #         Response: A response containing serialized data
    #         of the partially updated InternalUser instance.
    #     """
    #     user = users_service.get_by_id(pk=pk)
    #     if not user:
    #         return Response(
    #             data=Responses.error_response(
    #                 message=ResponseMessages.NO_DATA_FOUND.value
    #             ),
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #
    #     serializer = UsersSerializer(user, data=request.data, partial=True)
    #     if serializer.is_valid():
    #         updated_user = users_service.partial_update(user, serializer.validated_data)
    #         return Response(
    #             data=Responses.success_response(
    #                 message=ResponseMessages.REQUEST_SUCCESSFUL.value,
    #                 data=UsersSerializer(updated_user).data,
    #             ),
    #             status=status.HTTP_200_OK,
    #         )
    #     return Response(
    #         data=Responses.error_response(message=serializer.errors),
    #         status=status.HTTP_400_BAD_REQUEST,
    #     )
    #
    # @staticmethod
    # # @CustomJWTAuthentication.jwt_authenticated
    # # @ApiUtils.permission_required(feature="Users", permission="DELETE")
    # # @handle_exceptions
    # def destroy(request, pk: int) -> Response:  # pylint: disable=unused-argument
    #     """
    #     delete it a specific InternalUser instance.
    #
    #     Args:
    #         request: The HTTP request.
    #         pk (int): The primary key of the InternalUser instance to delete.
    #
    #     Returns:
    #         Response: A response indicating the success of the deletion.
    #     """
    #     user = users_service.get_by_id(pk=pk)
    #
    #     if not user:
    #         return Response(
    #             data=Responses.error_response(
    #                 message=ResponseMessages.NO_DATA_FOUND.value
    #             ),
    #             status=status.HTTP_404_NOT_FOUND,
    #         )
    #
    #     users_service.delete(user)
    #     return Response(
    #         data=Responses.success_response(
    #             message=ResponseMessages.DELETE_SUCCESSFUL.value
    #         ),
    #         status=status.HTTP_204_NO_CONTENT,
    #     )
