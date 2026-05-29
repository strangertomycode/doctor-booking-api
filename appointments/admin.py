from django.contrib import admin
from .models import AvailabilityRule, AvailabilitySlot, Appointment


@admin.register(AvailabilityRule)
class AvailabilityRuleAdmin(admin.ModelAdmin):
    list_display = ("doctor", "weekday", "start_time", "end_time", "is_active")
    list_filter = ("weekday", "is_active", "doctor")
    search_fields = ("doctor__full_name",)


@admin.register(AvailabilitySlot)
class AvailabilitySlotAdmin(admin.ModelAdmin):
    list_display = ("id", "doctor", "date", "start_time", "end_time", "is_booked")
    list_filter = ("date", "is_booked", "doctor")
    search_fields = ("doctor__full_name",)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "patient",
        "doctor",
        "status",
        "payment_status",
        "consultation_type",
        "created_at",
    )
    list_filter = ("status", "payment_status", "consultation_type")
    search_fields = ("patient__full_name", "doctor__full_name")
