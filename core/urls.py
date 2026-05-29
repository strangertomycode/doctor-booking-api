from django.contrib import admin
from django.urls import path, include

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path("", views.home),
    # Django Admin
    path("admin/", admin.site.urls),
    # Authentication + Users
    path("api/v1/auth/", include("accounts.urls")),
    # JWT Token Refresh
    path(
        "api/v1/auth/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    # Appointments
    path("api/v1/appointments/", include("appointments.urls")),
    # OpenAPI Schema
    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),
    # Swagger Docs
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    # ReDoc Docs
    path(
        "api/redoc/",
        SpectacularRedocView.as_view(url_name="schema"),
        name="redoc",
    ),
]
