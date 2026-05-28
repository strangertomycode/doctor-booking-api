from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date


class User(AbstractUser):
    username = None

    PATIENT = "patient"
    DOCTOR = "doctor"

    ROLE_CHOICES = [
        (PATIENT, "Patient"),
        (DOCTOR, "Doctor"),
    ]

    MALE = "male"
    FEMALE = "female"
    OTHER = "other"

    GENDER_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    ]

    A_POSITIVE = "A+"
    A_NEGATIVE = "A-"
    B_POSITIVE = "B+"
    B_NEGATIVE = "B-"
    O_POSITIVE = "O+"
    O_NEGATIVE = "O-"
    AB_POSITIVE = "AB+"
    AB_NEGATIVE = "AB-"

    BLOOD_GROUP_CHOICES = [
        (A_POSITIVE, "A+"),
        (A_NEGATIVE, "A-"),
        (B_POSITIVE, "B+"),
        (B_NEGATIVE, "B-"),
        (O_POSITIVE, "O+"),
        (O_NEGATIVE, "O-"),
        (AB_POSITIVE, "AB+"),
        (AB_NEGATIVE, "AB-"),
    ]

    email = models.EmailField(unique=True)

    full_name = models.CharField(max_length=255)

    phone_number = models.CharField(max_length=15, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)

    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True)

    blood_group = models.CharField(
        max_length=5, choices=BLOOD_GROUP_CHOICES, blank=True
    )

    medical_history = models.TextField(blank=True)

    allergies = models.TextField(blank=True)

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = []

    @property
    def age(self):

        if not self.date_of_birth:
            return None

        today = date.today()

        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )


class DoctorProfile(models.Model):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    SUSPENDED = "suspended"

    VERIFICATION_STATUS_CHOICES = [
        (PENDING, "Pending"),
        (APPROVED, "Approved"),
        (REJECTED, "Rejected"),
        (SUSPENDED, "Suspended"),
    ]

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name="doctor_profile",
    )

    specialization = models.CharField(max_length=100)

    qualification = models.CharField(max_length=255)

    years_of_experience = models.PositiveIntegerField()

    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2)

    bio = models.TextField(blank=True)

    hospital_name = models.CharField(max_length=255, blank=True)

    city = models.CharField(max_length=100, blank=True)

    verification_status = models.CharField(
        max_length=20, choices=VERIFICATION_STATUS_CHOICES, default=PENDING
    )

    verified_at = models.DateTimeField(null=True, blank=True)

    verified_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="verified_doctors",
    )

    rejection_reason = models.TextField(blank=True)

    def __str__(self):
        return f"Dr. {self.user.full_name}"

    @property
    def is_verified(self):
        return self.verification_status == self.APPROVED
