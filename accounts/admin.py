from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import (
    User,
    DoctorProfile,
)


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile

    fk_name = "user"

    can_delete = False

    extra = 0


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = [DoctorProfileInline]

    list_display = [
        "id",
        "email",
        "full_name",
        "role",
        "is_staff",
        "is_active",
    ]

    list_filter = [
        "role",
        "is_staff",
        "is_active",
    ]

    search_fields = [
        "email",
        "full_name",
    ]

    ordering = ["id"]

    readonly_fields = [
        "last_login",
        "date_joined",
    ]

    fieldsets = (
        (
            "Authentication Info",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal Info",
            {
                "fields": (
                    "full_name",
                    "phone_number",
                    "date_of_birth",
                    "gender",
                    "blood_group",
                    "medical_history",
                    "allergies",
                    "role",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "Important Dates",
            {
                "fields": (
                    "last_login",
                    "date_joined",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "full_name",
                    "role",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "user",
        "specialization",
        "verification_status",
        "years_of_experience",
        "consultation_fee",
    ]

    list_filter = [
        "verification_status",
        "specialization",
    ]

    search_fields = [
        "user__full_name",
        "user__email",
        "specialization",
    ]

    autocomplete_fields = [
        "user",
        "verified_by",
    ]

    fieldsets = (
        (
            "Doctor Info",
            {
                "fields": (
                    "user",
                    "specialization",
                    "qualification",
                    "years_of_experience",
                    "consultation_fee",
                    "bio",
                    "hospital_name",
                    "city",
                )
            },
        ),
        (
            "Verification",
            {
                "fields": (
                    "verification_status",
                    "verified_by",
                    "verified_at",
                    "rejection_reason",
                )
            },
        ),
    )

    actions = [
        "approve_doctors",
        "reject_doctors",
    ]

    readonly_fields = [
        "verified_at",
    ]

    @admin.action(description="Approve selected doctors")
    def approve_doctors(self, request, queryset):

        queryset.update(
            verification_status="approved",
            verified_by=request.user,
        )

    @admin.action(description="Reject selected doctors")
    def reject_doctors(self, request, queryset):

        queryset.update(
            verification_status="rejected",
            verified_by=request.user,
        )
