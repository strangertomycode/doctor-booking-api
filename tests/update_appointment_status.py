from base import APIClient

client = APIClient()


# Login as Doctor

login_payload = {"email": "doctor1@test.com", "password": "StrongPassword123"}

login_response = client.post(
    "/auth/login/",
    login_payload,
)

access = login_response.json()["access"]

client.set_token(access)


# =========================================
# Confirm Appointment
# =========================================

payload = {"status": "confirmed", "meeting_link": "https://meet.google.com/test"}

response = client.patch(
    "/appointments/2/update-status/",
    payload,
)

print(response.status_code)
print(response.json())


# =========================================
# Complete Appointment
# =========================================

payload = {"status": "completed", "prescription": "Paracetamol twice daily"}

response = client.patch(
    "/appointments/2/update-status/",
    payload,
)

print(response.status_code)
print(response.json())
