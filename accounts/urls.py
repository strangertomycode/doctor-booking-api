from django.urls import path

from .views import (
    RegisterView,
    EmailLoginView,
    MeView,
    DoctorListView,
    DoctorDetailView,
)

urlpatterns = [
    # Authentication
    path(
        "register/",
        RegisterView.as_view(),
        name="register",
    ),
    path(
        "login/",
        EmailLoginView.as_view(),
        name="login",
    ),
    # Current authenticated user
    path(
        "me/",
        MeView.as_view(),
        name="me",
    ),
    # Doctors
    path(
        "doctors/",
        DoctorListView.as_view(),
        name="doctor-list",
    ),
    path(
        "doctors/<int:pk>/",
        DoctorDetailView.as_view(),
        name="doctor-detail",
    ),
]
