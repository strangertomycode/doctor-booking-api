from django.urls import path

from .views import (
    # Availability
    AvailabilityRuleCreateView,
    MyAvailabilityRulesView,
    DoctorAvailableSlotsView,
    # Appointments
    AppointmentCreateView,
    MyAppointmentsView,
    AppointmentDetailView,
    AppointmentStatusUpdateView,
    CancelAppointmentView,
    # Dashboards
    DoctorAppointmentDashboardView,
    # Medical History
    PatientMedicalHistoryView,
)

urlpatterns = [
    # ==========================================
    # Availability Rules
    # ==========================================
    path(
        "availability-rules/",
        AvailabilityRuleCreateView.as_view(),
        name="availability-rule-create",
    ),
    path(
        "availability-rules/mine/",
        MyAvailabilityRulesView.as_view(),
        name="my-availability-rules",
    ),
    # ==========================================
    # Doctor Slots
    # ==========================================
    path(
        "doctors/<int:doctor_id>/slots/",
        DoctorAvailableSlotsView.as_view(),
        name="doctor-available-slots",
    ),
    # ==========================================
    # Appointments
    # ==========================================
    path(
        "",
        AppointmentCreateView.as_view(),
        name="appointment-create",
    ),
    path(
        "mine/",
        MyAppointmentsView.as_view(),
        name="my-appointments",
    ),
    path(
        "<int:pk>/",
        AppointmentDetailView.as_view(),
        name="appointment-detail",
    ),
    path(
        "<int:pk>/update-status/",
        AppointmentStatusUpdateView.as_view(),
        name="appointment-status-update",
    ),
    path(
        "<int:pk>/cancel/",
        CancelAppointmentView.as_view(),
        name="appointment-cancel",
    ),
    # ==========================================
    # Doctor Dashboard
    # ==========================================
    path(
        "doctor/dashboard/",
        DoctorAppointmentDashboardView.as_view(),
        name="doctor-appointment-dashboard",
    ),
    # ==========================================
    # Patient Medical History
    # ==========================================
    path(
        "patients/<int:patient_id>/medical-history/",
        PatientMedicalHistoryView.as_view(),
        name="patient-medical-history",
    ),
]
