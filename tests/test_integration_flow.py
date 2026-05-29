import requests
from datetime import datetime, timedelta

BASE_URL = "http://127.0.0.1:8000/api/v1"


# =========================================================
# API CLIENT
# =========================================================


class APIClient:
    def __init__(self):
        self.token = None

    def set_token(self, token):
        self.token = token

    @property
    def headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}

        return {}

    def get(self, endpoint, params=None):
        return requests.get(
            f"{BASE_URL}{endpoint}",
            headers=self.headers,
            params=params,
        )

    def post(self, endpoint, data=None):
        return requests.post(
            f"{BASE_URL}{endpoint}",
            json=data,
            headers=self.headers,
        )

    def patch(self, endpoint, data=None):
        return requests.patch(
            f"{BASE_URL}{endpoint}",
            json=data,
            headers=self.headers,
        )


# =========================================================
# HELPERS
# =========================================================


def print_response(title, response):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)

    print("STATUS:", response.status_code)

    try:
        print(response.json())
    except Exception:
        print(response.text)


# =========================================================
# TEST FLOW
# =========================================================

client = APIClient()

patient_id = None
doctor_id = None

patient_token = None
doctor_token = None

slot_id = None
appointment_id = None


# =========================================================
# REGISTER PATIENT
# =========================================================

patient_payload = {
    "email": "patient1@test.com",
    "password": "StrongPassword123",
    "password_confirm": "StrongPassword123",
    "full_name": "Rahul Patient",
    "phone_number": "9999999999",
    "gender": "male",
    "blood_group": "O+",
    "medical_history": "Diabetes",
    "allergies": "Dust allergy",
    "role": "patient",
}

response = client.post(
    "/auth/register/",
    patient_payload,
)

print_response("PATIENT REGISTER", response)

if response.status_code == 201:
    patient_id = response.json()["id"]


# =========================================================
# REGISTER DOCTOR
# =========================================================

doctor_payload = {
    "email": "doctor1@test.com",
    "password": "StrongPassword123",
    "password_confirm": "StrongPassword123",
    "full_name": "Dr Strange",
    "phone_number": "8888888888",
    "gender": "male",
    "role": "doctor",
    "doctor_profile": {
        "specialization": "Cardiology",
        "qualification": "MBBS, MD",
        "years_of_experience": 10,
        "consultation_fee": "1200.00",
        "bio": "Experienced cardiologist",
        "hospital_name": "Marvel Hospital",
        "city": "Kochi",
    },
}

response = client.post(
    "/auth/register/",
    doctor_payload,
)

print_response("DOCTOR REGISTER", response)

if response.status_code == 201:
    doctor_id = response.json()["id"]


# =========================================================
# PATIENT LOGIN
# =========================================================

patient_login_payload = {
    "email": "patient1@test.com",
    "password": "StrongPassword123",
}

response = client.post(
    "/auth/login/",
    patient_login_payload,
)

print_response("PATIENT LOGIN", response)

if response.status_code == 200:
    patient_token = response.json()["access"]


# =========================================================
# DOCTOR LOGIN
# =========================================================

doctor_login_payload = {
    "email": "doctor1@test.com",
    "password": "StrongPassword123",
}

response = client.post(
    "/auth/login/",
    doctor_login_payload,
)

print_response("DOCTOR LOGIN", response)

if response.status_code == 200:
    doctor_token = response.json()["access"]


# =========================================================
# DOCTOR CREATE AVAILABILITY
# =========================================================

client.set_token(doctor_token)

availability_payload = {
    # "weekday": datetime.now().weekday(),
    "weekday": 5,
    "start_time": "09:00:00",
    "end_time": "13:00:00",
    "slot_duration": 30,
    "break_between_slots": 10,
    "max_days_ahead": 30,
    "is_active": True,
}

response = client.post(
    "/appointments/availability-rules/",
    availability_payload,
)

print_response("DOCTOR CREATE AVAILABILITY", response)


# =========================================================
# LIST DOCTOR SLOTS
# =========================================================

client.set_token(patient_token)

date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

response = client.get(
    f"/appointments/doctors/{doctor_id}/slots/",
    params={"date": date},
)

print_response("LIST DOCTOR SLOTS", response)

if response.status_code == 200:
    data = response.json()

    if data["results"]:
        slot_id = data["results"][0]["id"]


# =========================================================
# BOOK APPOINTMENT
# =========================================================

appointment_payload = {
    "slot": slot_id,
    "appointment_reason": "Chest pain and breathing difficulty",
}

response = client.post(
    "/appointments/",
    appointment_payload,
)

print_response("BOOK APPOINTMENT", response)

if response.status_code == 201:
    appointment_id = response.json()["id"]


# =========================================================
# PATIENT MY APPOINTMENTS
# =========================================================

response = client.get("/appointments/mine/")

print_response("PATIENT MY APPOINTMENTS", response)


# =========================================================
# DOCTOR DASHBOARD
# =========================================================

client.set_token(doctor_token)

response = client.get("/appointments/doctor/dashboard/")

print_response("DOCTOR DASHBOARD", response)


# =========================================================
# UPDATE APPOINTMENT STATUS
# =========================================================

if appointment_id:
    update_payload = {"status": "confirmed"}

    response = client.patch(
        f"/appointments/{appointment_id}/update-status/",
        update_payload,
    )

    print_response("UPDATE APPOINTMENT STATUS", response)


# =========================================================
# MEDICAL HISTORY
# =========================================================

response = client.get(f"/appointments/patients/{patient_id}/medical-history/")

print_response("PATIENT MEDICAL HISTORY", response)


# =========================================================
# CANCEL APPOINTMENT
# =========================================================

client.set_token(patient_token)

if appointment_id:
    response = client.post(f"/appointments/{appointment_id}/cancel/")

    print_response("CANCEL APPOINTMENT", response)


# =========================================================
# NEGATIVE TEST - INVALID LOGIN
# =========================================================

invalid_payload = {
    "email": "wrong@test.com",
    "password": "wrongpassword",
}

response = client.post(
    "/auth/login/",
    invalid_payload,
)

print_response("INVALID LOGIN TEST", response)


# =========================================================
# NEGATIVE TEST - UNAUTHORIZED ACCESS
# =========================================================

unauthorized_client = APIClient()

response = unauthorized_client.get("/appointments/doctor/dashboard/")

print_response("UNAUTHORIZED ACCESS TEST", response)


# =========================================================
# NEGATIVE TEST - DOUBLE BOOKING
# =========================================================

if slot_id:
    client.set_token(patient_token)

    double_booking_payload = {
        "slot": slot_id,
        "reason": "Trying duplicate booking",
    }

    response = client.post(
        "/appointments/",
        double_booking_payload,
    )

    print_response("DOUBLE BOOKING TEST", response)


# =========================================================
# FINAL SUMMARY
# =========================================================

print("\n" + "=" * 60)
print("FINAL TEST SUMMARY")
print("=" * 60)

print("PATIENT ID:", patient_id)
print("DOCTOR ID:", doctor_id)
print("SLOT ID:", slot_id)
print("APPOINTMENT ID:", appointment_id)

print("\nTEST FLOW COMPLETED")
