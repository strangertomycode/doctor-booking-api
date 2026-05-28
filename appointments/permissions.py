from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from accounts.models import DoctorProfile
from .models import Appointment


class IsDoctor(BasePermission):
    message = "Only doctors can perform this action."

    def has_permission(self, request, view):

        return request.user.is_authenticated and request.user.role == "doctor"


class IsPatient(BasePermission):
    message = "Only patients can perform this action."

    def has_permission(self, request, view):

        return request.user.is_authenticated and request.user.role == "patient"


class IsVerifiedDoctor(BasePermission):
    message = "Only verified doctors can perform this action."

    def has_permission(self, request, view):

        if not request.user.is_authenticated:
            return False

        if request.user.role != "doctor":
            return False

        try:
            doctor_profile = request.user.doctor_profile

            return doctor_profile.verification_status == DoctorProfile.APPROVED

        except DoctorProfile.DoesNotExist:
            return False


class IsAppointmentOwner(BasePermission):
    message = "You do not have permission to access this appointment."

    def has_object_permission(self, request, view, obj):

        return obj.patient == request.user or obj.doctor == request.user


class IsAppointmentPatient(BasePermission):
    message = "Only the patient who booked this appointment can perform this action."

    def has_object_permission(self, request, view, obj):

        return obj.patient == request.user


class IsAppointmentDoctor(BasePermission):
    message = "Only the assigned doctor can perform this action."

    def has_object_permission(self, request, view, obj):

        return obj.doctor == request.user


class CanManageAppointmentStatus(BasePermission):
    message = "Only the assigned doctor can manage appointment status."

    def has_object_permission(self, request, view, obj):

        return request.user.role == "doctor" and obj.doctor == request.user


class CanCancelAppointment(BasePermission):
    message = "You cannot cancel this appointment."

    def has_object_permission(self, request, view, obj):

        if obj.status in [
            Appointment.CANCELLED,
            Appointment.COMPLETED,
        ]:
            return False

        return obj.patient == request.user or obj.doctor == request.user


class ReadOnly(BasePermission):
    def has_permission(self, request, view):

        return request.method in SAFE_METHODS
