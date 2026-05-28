from django.db.models import Q
from django.utils import timezone

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from django_filters.rest_framework import DjangoFilterBackend

from .models import (
    AvailabilityRule,
    AvailabilitySlot,
    Appointment,
)

from .serializers import (
    AvailabilityRuleSerializer,
    AvailabilitySlotSerializer,
    AppointmentSerializer,
    AppointmentStatusUpdateSerializer,
)

from .permissions import (
    IsDoctor,
    IsPatient,
    IsVerifiedDoctor,
    IsAppointmentOwner,
    CanManageAppointmentStatus,
    CanCancelAppointment,
)

from accounts.models import (
    User,
    DoctorProfile,
)


class AvailabilityRuleCreateView(generics.CreateAPIView):
    serializer_class = AvailabilityRuleSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsDoctor,
        IsVerifiedDoctor,
    ]

    def perform_create(self, serializer):

        serializer.save(doctor=self.request.user)


class MyAvailabilityRulesView(generics.ListAPIView):
    serializer_class = AvailabilityRuleSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsDoctor,
    ]

    def get_queryset(self):

        return AvailabilityRule.objects.filter(doctor=self.request.user).order_by(
            "weekday",
            "start_time",
        )


class DoctorAvailableSlotsView(generics.ListAPIView):
    serializer_class = AvailabilitySlotSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["date"]

    def get_queryset(self):

        doctor_id = self.kwargs["doctor_id"]

        return (
            AvailabilitySlot.objects.filter(
                doctor_id=doctor_id,
                doctor__role="doctor",
                doctor__doctor_profile__verification_status=DoctorProfile.APPROVED,
                is_booked=False,
                date__gte=timezone.localdate(),
            )
            .select_related(
                "doctor",
                "doctor__doctor_profile",
            )
            .order_by(
                "date",
                "start_time",
            )
        )


class AppointmentCreateView(generics.CreateAPIView):
    serializer_class = AppointmentSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsPatient,
    ]


class MyAppointmentsView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        "status",
        "payment_status",
        "consultation_type",
    ]

    def get_queryset(self):

        user = self.request.user

        queryset = Appointment.objects.select_related(
            "patient",
            "doctor",
            "doctor__doctor_profile",
            "slot",
        )

        if user.role == "doctor":
            queryset = queryset.filter(doctor=user)

        else:
            queryset = queryset.filter(patient=user)

        return queryset.order_by("-created_at")


class AppointmentDetailView(generics.RetrieveAPIView):
    serializer_class = AppointmentSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsAppointmentOwner,
    ]

    def get_queryset(self):

        return Appointment.objects.select_related(
            "patient",
            "doctor",
            "doctor__doctor_profile",
            "slot",
        )


class AppointmentStatusUpdateView(generics.UpdateAPIView):
    serializer_class = AppointmentStatusUpdateSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsDoctor,
        CanManageAppointmentStatus,
    ]

    http_method_names = [
        "patch",
    ]

    def get_queryset(self):

        return Appointment.objects.filter(doctor=self.request.user)


class CancelAppointmentView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        CanCancelAppointment,
    ]

    def post(self, request, pk):

        try:
            appointment = Appointment.objects.select_related("slot").get(pk=pk)

        except Appointment.DoesNotExist:
            return Response(
                {"detail": "Appointment not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        self.check_object_permissions(request, appointment)

        appointment.status = Appointment.CANCELLED

        appointment.cancelled_by = request.user

        appointment.cancelled_at = timezone.now()

        appointment.cancellation_reason = request.data.get(
            "cancellation_reason",
            "",
        )

        appointment.slot.is_booked = False
        appointment.slot.save()

        appointment.save()

        return Response(
            {"detail": "Appointment cancelled successfully."},
            status=status.HTTP_200_OK,
        )


class DoctorAppointmentDashboardView(generics.ListAPIView):
    serializer_class = AppointmentSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsDoctor,
        IsVerifiedDoctor,
    ]

    filter_backends = [DjangoFilterBackend]

    filterset_fields = [
        "status",
        "payment_status",
        "consultation_type",
    ]

    def get_queryset(self):

        today = timezone.localdate()

        return (
            Appointment.objects.filter(
                doctor=self.request.user,
                slot__date__gte=today,
            )
            .select_related(
                "patient",
                "doctor",
                "doctor__doctor_profile",
                "slot",
            )
            .order_by(
                "slot__date",
                "slot__start_time",
            )
        )


class PatientMedicalHistoryView(generics.RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsDoctor,
        IsVerifiedDoctor,
    ]

    def get(self, request, patient_id):

        try:
            patient = User.objects.get(
                id=patient_id,
                role="patient",
            )

        except User.DoesNotExist:
            return Response(
                {"detail": "Patient not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        has_appointment = Appointment.objects.filter(
            patient=patient,
            doctor=request.user,
        ).exists()

        if not has_appointment:
            return Response(
                {"detail": "You do not have access to this patient's medical history."},
                status=status.HTTP_403_FORBIDDEN,
            )

        data = {
            "patient_id": patient.id,
            "full_name": patient.full_name,
            "blood_group": patient.blood_group,
            "medical_history": patient.medical_history,
            "allergies": patient.allergies,
        }

        return Response(data)
