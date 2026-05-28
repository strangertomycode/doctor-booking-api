from rest_framework.serializers import (
    ModelSerializer,
    ReadOnlyField,
    CharField,
    ValidationError,
)
from .models import User, DoctorProfile


class DoctorProfileSerializer(ModelSerializer):
    class Meta:
        model = DoctorProfile

        fields = [
            "id",
            "specialization",
            "qualification",
            "years_of_experience",
            "consultation_fee",
            "bio",
            "hospital_name",
            "city",
            "is_verified",
        ]

        read_only_fields = ["is_verified"]


class UserSerializer(ModelSerializer):
    age = ReadOnlyField()

    doctor_profile = DoctorProfileSerializer(read_only=True)

    class Meta:
        model = User

        fields = [
            "id",
            "email",
            "full_name",
            "phone_number",
            "date_of_birth",
            "age",
            "gender",
            "blood_group",
            "medical_history",
            "allergies",
            "role",
            "doctor_profile",
        ]


class RegisterSerializer(ModelSerializer):
    password = CharField(write_only=True, min_length=8)

    doctor_profile = DoctorProfileSerializer(required=False)

    class Meta:
        model = User

        fields = [
            "email",
            "password",
            "full_name",
            "phone_number",
            "date_of_birth",
            "gender",
            "blood_group",
            "medical_history",
            "allergies",
            "role",
            "doctor_profile",
        ]

    def validate(self, data):

        role = data.get("role")

        doctor_profile = data.get("doctor_profile")

        if role == User.DOCTOR and not doctor_profile:
            raise ValidationError(
                {"doctor_profile": "Doctor profile data is required for doctors."}
            )

        return data

    def create(self, validated_data):

        doctor_profile_data = validated_data.pop("doctor_profile", None)

        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)

        if user.role == User.DOCTOR and doctor_profile_data:
            DoctorProfile.objects.create(user=user, **doctor_profile_data)

        return user
