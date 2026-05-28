from django.db import models
from django.conf import settings


class AvailabilityRule(models.Model):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6

    WEEKDAY_CHOICES = [
        (MONDAY, "Monday"),
        (TUESDAY, "Tuesday"),
        (WEDNESDAY, "Wednesday"),
        (THURSDAY, "Thursday"),
        (FRIDAY, "Friday"),
        (SATURDAY, "Saturday"),
        (SUNDAY, "Sunday"),
    ]

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="availability_rules",
    )

    weekday = models.IntegerField(choices=WEEKDAY_CHOICES)

    start_time = models.TimeField()

    end_time = models.TimeField()

    slot_duration = models.PositiveIntegerField(
        default=30, help_text="Duration of each slot in minutes."
    )

    break_between_slots = models.PositiveIntegerField(
        default=0, help_text="Break between slots in minutes."
    )

    max_days_ahead = models.PositiveIntegerField(
        default=30, help_text="Generate slots this many days ahead."
    )

    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = [
            "weekday",
            "start_time",
        ]

        unique_together = (
            "doctor",
            "weekday",
            "start_time",
            "end_time",
        )

    def __str__(self):

        return (
            f"{self.doctor.full_name} - "
            f"{self.get_weekday_display()} "
            f"({self.start_time} - {self.end_time})"
        )


class AvailabilitySlot(models.Model):
    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="availability_slots",
    )

    rule = models.ForeignKey(
        AvailabilityRule,
        on_delete=models.CASCADE,
        related_name="generated_slots",
    )

    date = models.DateField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    is_booked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = [
            "date",
            "start_time",
        ]

        unique_together = (
            "doctor",
            "date",
            "start_time",
        )

    def __str__(self):

        return f"{self.doctor.full_name} - {self.date} {self.start_time}"


class Appointment(models.Model):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    MISSED = "missed"

    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (CONFIRMED, "Confirmed"),
        (CANCELLED, "Cancelled"),
        (COMPLETED, "Completed"),
        (MISSED, "Missed"),
    ]

    UNPAID = "unpaid"
    PAID = "paid"
    REFUNDED = "refunded"

    PAYMENT_STATUS_CHOICES = [
        (UNPAID, "Unpaid"),
        (PAID, "Paid"),
        (REFUNDED, "Refunded"),
    ]

    ONLINE = "online"
    IN_PERSON = "in_person"

    CONSULTATION_TYPE_CHOICES = [
        (ONLINE, "Online"),
        (IN_PERSON, "In Person"),
    ]

    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_appointments",
    )

    doctor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="doctor_appointments",
    )

    slot = models.OneToOneField(
        AvailabilitySlot,
        on_delete=models.CASCADE,
        related_name="appointment",
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default=UNPAID,
    )

    consultation_type = models.CharField(
        max_length=20,
        choices=CONSULTATION_TYPE_CHOICES,
        default=IN_PERSON,
    )

    appointment_reason = models.TextField()

    symptoms = models.TextField(blank=True)

    notes = models.TextField(blank=True)

    prescription = models.TextField(blank=True)

    meeting_link = models.URLField(blank=True)

    cancellation_reason = models.TextField(blank=True)

    cancelled_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="cancelled_appointments",
    )

    cancelled_at = models.DateTimeField(null=True, blank=True)

    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):

        return (
            f"Appointment - {self.patient.full_name} with Dr. {self.doctor.full_name}"
        )
