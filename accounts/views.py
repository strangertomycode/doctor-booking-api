from rest_framework import permissions
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema

from .models import User, DoctorProfile
from .serializers import (
    RegisterSerializer,
    UserSerializer,
)
from rest_framework.exceptions import AuthenticationFailed


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD

    def validate(self, attrs):

        credentials = {
            "email": attrs.get("email"),
            "password": attrs.get("password"),
        }

        user = authenticate(request=self.context.get("request"), **credentials)

        if user is None or not user.is_active:
            raise AuthenticationFailed("Invalid email or password.")

        refresh = self.get_token(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": UserSerializer(user).data,
        }


@extend_schema(tags=["Auth"])
class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailTokenObtainPairSerializer


@extend_schema(tags=["Auth"])
class RegisterView(CreateAPIView):
    serializer_class = RegisterSerializer

    permission_classes = [permissions.AllowAny]


@extend_schema(tags=["User"])
class MeView(RetrieveAPIView):
    permission_classes = [permissions.IsAuthenticated]

    serializer_class = UserSerializer

    def get(self, request):

        serializer = UserSerializer(request.user)

        return Response(serializer.data)

    def patch(self, request):

        user = request.user

        serializer = UserSerializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response(serializer.data)


@extend_schema(tags=["Doctors"])
class DoctorListView(ListAPIView):
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):

        return User.objects.filter(
            role=User.DOCTOR, doctor_profile__verification_status=DoctorProfile.APPROVED
        ).select_related("doctor_profile")


@extend_schema(tags=["Doctors"])
class DoctorDetailView(RetrieveAPIView):
    serializer_class = UserSerializer

    permission_classes = [permissions.IsAuthenticated]

    queryset = User.objects.filter(
        role=User.DOCTOR, doctor_profile__verification_status=DoctorProfile.APPROVED
    ).select_related("doctor_profile")
