"""appointment_booking_system_app URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appointment_booking_system_app.views import (
    DistrictViewSet,
    DivisionViewSet,
    ThanaViewSet,
    UserSessionManagementViewSet,
    UserViewSet,
)

urlpatterns = [
    path(
        "division/list/",
        DivisionViewSet.as_view({"get": "list"}),
        name="division-list",
    ),
    path(
        "division/create/",
        DivisionViewSet.as_view({"post": "create"}),
        name="division-create",
    ),
    path(
        "division/<int:pk>/",
        DivisionViewSet.as_view({"get": "retrieve"}),
        name="division-retrieve",
    ),
    path(
        "division/<int:pk>/partial/update/",
        DivisionViewSet.as_view({"patch": "partial_update"}),
        name="division-partial-update",
    ),
    path(
        "division/<int:pk>/delete/",
        DivisionViewSet.as_view({"delete": "destroy"}),
        name="division-delete",
    ),
    path(
        "district/list/",
        DistrictViewSet.as_view({"get": "list"}),
        name="district-list",
    ),
    path(
        "district/create/",
        DistrictViewSet.as_view({"post": "create"}),
        name="district-create",
    ),
    path(
        "district/<int:pk>/",
        DistrictViewSet.as_view({"get": "retrieve"}),
        name="district-retrieve",
    ),
    path(
        "district/<int:pk>/partial/update/",
        DistrictViewSet.as_view({"patch": "partial_update"}),
        name="district-partial-update",
    ),
    path(
        "district/<int:pk>/delete/",
        DistrictViewSet.as_view({"delete": "destroy"}),
        name="district-delete",
    ),
    path(
        "thana/list/",
        ThanaViewSet.as_view({"get": "list"}),
        name="thana-list",
    ),
    path(
        "thana/create/",
        ThanaViewSet.as_view({"post": "create"}),
        name="thana-create",
    ),
    path(
        "thana/<int:pk>/",
        ThanaViewSet.as_view({"get": "retrieve"}),
        name="thana-retrieve",
    ),
    path(
        "thana/<int:pk>/partial/update/",
        ThanaViewSet.as_view({"patch": "partial_update"}),
        name="thana-partial-update",
    ),
    path(
        "thana/<int:pk>/delete/",
        ThanaViewSet.as_view({"delete": "destroy"}),
        name="thana-delete",
    ),
    path(
        "user/list/",
        UserViewSet.as_view({"get": "list"}),
        name="user-list",
    ),
    path(
        "user/register/",
        UserViewSet.as_view({"post": "create"}),
        name="user-create",
    ),
    path(
        "user/<int:pk>/",
        UserViewSet.as_view({"get": "retrieve"}),
        name="user-retrieve",
    ),
    path(
        "user/<int:pk>/partial/update/",
        UserViewSet.as_view({"patch": "partial_update"}),
        name="user-partial-update",
    ),
    path(
        "user/<int:pk>/delete/",
        UserViewSet.as_view({"delete": "destroy"}),
        name="user-delete",
    ),
    path(
        "user/login/",
        UserSessionManagementViewSet.as_view({"post": "login"}),
        name="user_login",
    ),
    path(
        "user/logout/",
        UserSessionManagementViewSet.as_view({"post": "logout"}),
        name="user_logout",
    ),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
