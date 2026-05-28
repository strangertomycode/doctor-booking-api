from datetime import datetime, timedelta

from django.db import transaction
from django.utils import timezone

from rest_framework.serializers import (
    ModelSerializer,
    CharField,
    IntegerField,
    DecimalField,
    ValidationError,
    SerializerMethodField,
    Serializer,
)

from .models import (
    AvailabilityRule,
    AvailabilitySlot,
    Appointment,
)

from accounts.models import (
    User,
    DoctorProfile,
)


class DoctorBasicSerializer(ModelSerializer):
    specialization = CharField(source="doctor_profile.specialization", read_only=True)

    qualification = CharField(source="doctor_profile.qualification", read_only=True)

    years_of_experience = IntegerField(
        source="doctor_profile.years_of_experience", read_only=True
    )

    consultation_fee = DecimalField(
        source="doctor_profile.consultation_fee",
        max_digits=8,
        decimal_places=2,
        read_only=True,
    )

    hospital_name = CharField(source="doctor_profile.hospital_name", read_only=True)

    class Meta:
        model = User

        fields = [
            "id",
            "full_name",
            "email",
            "specialization",
            "qualification",
            "years_of_experience",
            "consultation_fee",
            "hospital_name",
        ]


class AvailabilityRuleSerializer(ModelSerializer):
    doctor_name = CharField(source="doctor.full_name", read_only=True)

    class Meta:
        model = AvailabilityRule

        fields = [
            "id",
            "doctor",
            "doctor_name",
            "weekday",
            "start_time",
            "end_time",
            "slot_duration",
            "break_between_slots",
            "max_days_ahead",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "doctor",
            "doctor_name",
            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):

        start_time = attrs.get("start_time")
        end_time = attrs.get("end_time")

        if start_time >= end_time:
            raise ValidationError("End time must be after start time.")

        slot_duration = attrs.get("slot_duration")

        if slot_duration <= 0:
            raise ValidationError("Slot duration must be greater than 0.")

        return attrs

    def create(self, validated_data):

        rule = AvailabilityRule.objects.create(**validated_data)

        self.generate_slots(rule)

        return rule

    def generate_slots(self, rule):

        today = timezone.localdate()

        for day_offset in range(rule.max_days_ahead):
            current_date = today + timedelta(days=day_offset)

            if current_date.weekday() != rule.weekday:
                continue

            current_time = datetime.combine(current_date, rule.start_time)

            end_datetime = datetime.combine(current_date, rule.end_time)

            while current_time < end_datetime:
                slot_start = current_time.time()

                slot_end_datetime = current_time + timedelta(minutes=rule.slot_duration)

                slot_end = slot_end_datetime.time()

                if slot_end_datetime > end_datetime:
                    break

                AvailabilitySlot.objects.get_or_create(
                    doctor=rule.doctor,
                    rule=rule,
                    date=current_date,
                    start_time=slot_start,
                    defaults={
                        "end_time": slot_end,
                    },
                )

                current_time = slot_end_datetime + timedelta(
                    minutes=rule.break_between_slots
                )


class AvailabilitySlotSerializer(ModelSerializer):
    doctor = DoctorBasicSerializer(read_only=True)

    weekday = SerializerMethodField()

    class Meta:
        model = AvailabilitySlot

        fields = [
            "id",
            "doctor",
            "weekday",
            "date",
            "start_time",
            "end_time",
            "is_booked",
        ]

    def get_weekday(self, obj) -> str:

        return obj.date.strftime("%A")


class AppointmentSerializer(ModelSerializer):
    patient_name = CharField(source="patient.full_name", read_only=True)

    doctor = DoctorBasicSerializer(read_only=True)

    slot_details = AvailabilitySlotSerializer(source="slot", read_only=True)

    class Meta:
        model = Appointment

        fields = [
            "id",
            "patient",
            "patient_name",
            "doctor",
            "slot",
            "slot_details",
            "status",
            "payment_status",
            "consultation_type",
            "appointment_reason",
            "symptoms",
            "notes",
            "prescription",
            "meeting_link",
            "cancellation_reason",
            "cancelled_at",
            "completed_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "patient",
            "doctor",
            "status",
            "payment_status",
            "meeting_link",
            "cancelled_at",
            "completed_at",
            "created_at",
            "updated_at",
        ]

    def validate_slot(self, slot):

        if slot.is_booked:
            raise ValidationError("This slot is already booked.")

        if slot.date < timezone.localdate():
            raise ValidationError("Cannot book past slots.")

        if slot.doctor.doctor_profile.verification_status != DoctorProfile.APPROVED:
            raise ValidationError("Doctor is not verified.")

        return slot

    @transaction.atomic
    def create(self, validated_data):

        slot = AvailabilitySlot.objects.select_for_update().get(
            id=validated_data["slot"].id
        )

        if slot.is_booked:
            raise ValidationError("This slot has already been booked.")

        slot.is_booked = True
        slot.save()

        appointment = Appointment.objects.create(
            patient=self.context["request"].user,
            doctor=slot.doctor,
            slot=slot,
            **validated_data,
        )

        return appointment


class AppointmentStatusUpdateSerializer(ModelSerializer):
    class Meta:
        model = Appointment

        fields = [
            "status",
            "payment_status",
            "prescription",
            "meeting_link",
            "notes",
            "cancellation_reason",
        ]

    def validate(self, attrs):

        appointment = self.instance

        new_status = attrs.get("status", appointment.status)

        if appointment.status == Appointment.CANCELLED:
            raise ValidationError("Cancelled appointments cannot be updated.")

        if appointment.status == Appointment.COMPLETED:
            raise ValidationError("Completed appointments cannot be updated.")

        if new_status == Appointment.COMPLETED and not attrs.get("prescription"):
            raise ValidationError(
                "Prescription is required when completing appointment."
            )

        return attrs

    def update(self, instance, validated_data):

        new_status = validated_data.get("status")

        if new_status == Appointment.CANCELLED:
            instance.cancelled_at = timezone.now()

            instance.slot.is_booked = False
            instance.slot.save()

        if new_status == Appointment.COMPLETED:
            instance.completed_at = timezone.now()

        return super().update(instance, validated_data)


class CancelAppointmentSerializer(Serializer):
    cancellation_reason = CharField(
        required=False,
        allow_blank=True,
    )


class PatientMedicalHistorySerializer(Serializer):
    patient_id = IntegerField()

    full_name = CharField()

    blood_group = CharField()

    medical_history = CharField()

    allergies = CharField()
