from django.utils import timezone

from rest_framework import status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    CreateAPIView,
    UpdateAPIView,
)
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
    CancelAppointmentSerializer,
    PatientMedicalHistorySerializer,
)

from .permissions import (
    IsDoctor,
    IsPatient,
    IsVerifiedDoctor,
    IsAppointmentOwner,
    CanManageAppointmentStatus,
    CanCancelAppointment,
)
from drf_spectacular.utils import extend_schema

from accounts.models import (
    User,
    DoctorProfile,
)

from rest_framework.exceptions import PermissionDenied


@extend_schema(tags=["Scheduling"])
class AvailabilityRuleCreateView(CreateAPIView):
    serializer_class = AvailabilityRuleSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsDoctor,
        IsVerifiedDoctor,
    ]

    def perform_create(self, serializer):
        user = self.request.user

        if user.role != "doctor":
            raise PermissionDenied("Only doctors can create availability rules")

        serializer.save(doctor=user.doctor_profile)


@extend_schema(tags=["Scheduling"])
class MyAvailabilityRulesView(ListAPIView):
    serializer_class = AvailabilityRuleSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsDoctor,
    ]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return AvailabilitySlot.objects.none()

        return AvailabilityRule.objects.filter(doctor=self.request.user).order_by(
            "weekday",
            "start_time",
        )


@extend_schema(tags=["Scheduling"])
class DoctorAvailableSlotsView(ListAPIView):
    serializer_class = AvailabilitySlotSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    filter_backends = [DjangoFilterBackend]

    filterset_fields = ["date"]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return AvailabilitySlot.objects.none()

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


@extend_schema(tags=["Appointments"])
class AppointmentCreateView(CreateAPIView):
    serializer_class = AppointmentSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsPatient,
    ]


@extend_schema(tags=["Appointments"])
class MyAppointmentsView(ListAPIView):
    queryset = Appointment.objects.none()
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

        if getattr(self, "swagger_fake_view", False):
            return AvailabilitySlot.objects.none()

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


@extend_schema(tags=["Appointments"])
class AppointmentDetailView(RetrieveAPIView):
    queryset = Appointment.objects.none()
    serializer_class = AppointmentSerializer

    permission_classes = [
        permissions.IsAuthenticated,
        IsAppointmentOwner,
    ]

    def get_queryset(self):

        if getattr(self, "swagger_fake_view", False):
            return AvailabilitySlot.objects.none()

        return Appointment.objects.select_related(
            "patient",
            "doctor",
            "doctor__doctor_profile",
            "slot",
        )


@extend_schema(tags=["Appointments"])
class AppointmentStatusUpdateView(UpdateAPIView):
    queryset = Appointment.objects.none()
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

        if getattr(self, "swagger_fake_view", False):
            return AvailabilitySlot.objects.none()

        return Appointment.objects.filter(doctor=self.request.user)


@extend_schema(tags=["Appointments"])
class CancelAppointmentView(APIView):
    permission_classes = [
        permissions.IsAuthenticated,
        CanCancelAppointment,
    ]

    serializer_class = CancelAppointmentSerializer

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


@extend_schema(tags=["Doctor Dashboard"])
class DoctorAppointmentDashboardView(ListAPIView):
    queryset = Appointment.objects.none()
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

        if getattr(self, "swagger_fake_view", False):
            return AvailabilitySlot.objects.none()

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


@extend_schema(tags=["Medical Records"])
class PatientMedicalHistoryView(RetrieveAPIView):
    permission_classes = [
        permissions.IsAuthenticated,
        IsDoctor,
        IsVerifiedDoctor,
    ]

    serializer_class = PatientMedicalHistorySerializer

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
