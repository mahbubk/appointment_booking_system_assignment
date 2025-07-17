"""appointment_booking_system_app URL Configuration"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appointment_booking_system_app.views import (
    DistrictViewSet,
    DivisionViewSet,
    DoctorProfileViewSet,
    SpecializationViewSet,
    ThanaViewSet,
    UserSessionManagementViewSet,
    UserViewSet,
    TimeSlotViewSet, AppointmentViewSet, AccessTokenFromRefreshToken,
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
        "specialization/list/",
        SpecializationViewSet.as_view({"get": "list"}),
        name="specialization-list",
    ),
    path(
        "specialization/create/",
        SpecializationViewSet.as_view({"post": "create"}),
        name="specialization-create",
    ),
    path(
        "specialization/<int:pk>/",
        SpecializationViewSet.as_view({"get": "retrieve"}),
        name="specialization-retrieve",
    ),
    path(
        "specialization/<int:pk>/partial/update/",
        SpecializationViewSet.as_view({"patch": "partial_update"}),
        name="specialization-partial-update",
    ),
    path(
        "specialization/<int:pk>/delete/",
        SpecializationViewSet.as_view({"delete": "destroy"}),
        name="specialization-delete",
    ),
    path(
        "doctor/profile/list/",
        DoctorProfileViewSet.as_view({"get": "list"}),
        name="doctor-profile-list",
    ),
    path(
        "doctor/profile/create/",
        DoctorProfileViewSet.as_view({"post": "create"}),
        name="doctor-profile-create",
    ),
    path(
        "doctor/profile/<int:pk>/",
        DoctorProfileViewSet.as_view({"get": "retrieve"}),
        name="doctor-profile-retrieve",
    ),
    path(
        "doctor/profile/<int:pk>/partial/update/",
        DoctorProfileViewSet.as_view({"patch": "partial_update"}),
        name="doctor-profile-partial-update",
    ),
    path(
        "doctor/profile/<int:pk>/delete/",
        DoctorProfileViewSet.as_view({"delete": "destroy"}),
        name="doctor-profile-delete",
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
    path(
        "refresh/token/",
        AccessTokenFromRefreshToken.as_view({"post": "create"}),
        name="refresh_token",
    ),
    path(
        "time/slot/list/",
        TimeSlotViewSet.as_view({"get": "list"}),
        name="time-slot-list",
    ),
    path(
        "time/slot/create/",
        TimeSlotViewSet.as_view({"post": "create"}),
        name="time-slot-create",
    ),
    path(
        "time/slot/<int:pk>/",
        TimeSlotViewSet.as_view({"get": "retrieve"}),
        name="time-slot-retrieve",
    ),
    path(
        "time/slot/<int:pk>/partial/update/",
        TimeSlotViewSet.as_view({"patch": "partial_update"}),
        name="time-slot-partial-update",
    ),
    path(
        "time/slot/<int:pk>/delete/",
        TimeSlotViewSet.as_view({"delete": "destroy"}),
        name="time-slot-delete",
    ),
    path(
        "appointment/list/",
        AppointmentViewSet.as_view({"get": "list"}),
        name="appointment-slot-list",
    ),
    path(
        "appointment/create/",
        AppointmentViewSet.as_view({"post": "create"}),
        name="appointment-slot-create",
    ),
    path(
        "appointment/<int:pk>/",
        AppointmentViewSet.as_view({"get": "retrieve"}),
        name="appointment-slot-retrieve",
    ),
    path(
        "appointment/<int:pk>/partial/update/",
        AppointmentViewSet.as_view({"patch": "partial_update"}),
        name="appointment-slot-partial-update",
    ),
    path(
        "appointment/<int:pk>/delete/",
        AppointmentViewSet.as_view({"delete": "destroy"}),
        name="appointment-slot-delete",
    ),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
