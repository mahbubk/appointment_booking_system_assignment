from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from appointment_booking_system_app.views import DivisionViewSet, UserViewSet

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
        "user/register/",
        UserViewSet.as_view({"post": "create"}),
        name="user-create",
    ),
]


urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
