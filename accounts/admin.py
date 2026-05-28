from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, DoctorProfile


class DoctorProfileInline(admin.StackedInline):
    model = DoctorProfile

    fk_name = "user"

    can_delete = False

    extra = 0

    exclude = ["verified_by"]


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    inlines = [DoctorProfileInline]

    list_display = [
        "id",
        "email",
        "full_name",
        "role",
        "gender",
        "phone_number",
        "is_staff",
        "is_active",
    ]

    list_filter = [
        "role",
        "gender",
        "is_staff",
        "is_active",
    ]

    search_fields = [
        "email",
        "full_name",
        "phone_number",
    ]

    ordering = ["id"]

    readonly_fields = [
        "last_login",
        "date_joined",
    ]

    fieldsets = (
        (
            "Authentication",
            {
                "fields": (
                    "email",
                    "password",
                )
            },
        ),
        (
            "Personal Information",
            {
                "fields": (
                    "full_name",
                    "phone_number",
                    "date_of_birth",
                    "gender",
                    "blood_group",
                    "medical_history",
                    "allergies",
                )
            },
        ),
        (
            "Role Information",
            {"fields": ("role",)},
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
                    "full_name",
                    "role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    filter_horizontal = (
        "groups",
        "user_permissions",
    )


@admin.register(DoctorProfile)
class DoctorProfileAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "get_doctor_name",
        "specialization",
        "qualification",
        "years_of_experience",
        "hospital_name",
        "city",
        "verification_status",
    ]

    list_filter = [
        "verification_status",
        "specialization",
        "city",
    ]

    search_fields = [
        "user__full_name",
        "user__email",
        "specialization",
        "hospital_name",
    ]

    ordering = ["id"]

    readonly_fields = [
        "verified_at",
    ]

    actions = [
        "approve_doctors",
        "reject_doctors",
        "suspend_doctors",
    ]

    def get_doctor_name(self, obj):
        return obj.user.full_name

    get_doctor_name.short_description = "Doctor"

    def approve_doctors(self, request, queryset):

        queryset.update(verification_status=DoctorProfile.APPROVED)

    approve_doctors.short_description = "Approve selected doctors"

    def reject_doctors(self, request, queryset):

        queryset.update(verification_status=DoctorProfile.REJECTED)

    reject_doctors.short_description = "Reject selected doctors"

    def suspend_doctors(self, request, queryset):

        queryset.update(verification_status=DoctorProfile.SUSPENDED)

    suspend_doctors.short_description = "Suspend selected doctors"
