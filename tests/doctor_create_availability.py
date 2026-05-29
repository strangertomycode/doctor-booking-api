from base import APIClient

client = APIClient()


# =========================================
# Login as Doctor
# =========================================

login_payload = {"email": "doctor1@test.com", "password": "StrongPassword123"}

login_response = client.post(
    "/auth/login/",
    login_payload,
)

print(login_response.status_code)
print(login_response.json())

access = login_response.json()["access"]

client.set_token(access)


# =========================================
# Create Recurring Availability
# =========================================

availability_payload = {
    "weekday": 0,
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

print(response.status_code)
print(response.json())
