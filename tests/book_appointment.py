from base import APIClient

client = APIClient()


# =========================================
# Login as Patient
# =========================================

login_payload = {"email": "patient1@test.com", "password": "StrongPassword123"}

login_response = client.post(
    "/auth/login/",
    login_payload,
)

access = login_response.json()["access"]

client.set_token(access)


# =========================================
# Book Appointment
# =========================================

appointment_payload = {
    "slot": 26,
    "consultation_type": "online",
    "appointment_reason": "Chest pain",
    "symptoms": "Pain while breathing",
}

response = client.post(
    "/appointments/",
    appointment_payload,
)

print(response.status_code)
try:
    print(response.json())
except Exception:
    print(response.text)
