from base import APIClient

client = APIClient()


# =========================================
# Invalid Login
# =========================================

payload = {"email": "wrong@test.com", "password": "wrongpass"}

response = client.post(
    "/auth/login/",
    payload,
)

print("INVALID LOGIN")
print(response.status_code)
try:
    print(response.json())
except Exception:
    print(response.text)
print()


# =========================================
# Book Already Booked Slot
# =========================================

login_payload = {"email": "patient1@test.com", "password": "StrongPassword123"}

login_response = client.post(
    "/auth/login/",
    login_payload,
)

access = login_response.json()["access"]

client.set_token(access)


appointment_payload = {
    "slot": 7,
    "consultation_type": "online",
    "appointment_reason": "Trying duplicate booking",
}

response = client.post(
    "/appointments/",
    appointment_payload,
)

print("DOUBLE BOOK TEST")
print(response.status_code)
print(response.json())
print()


# =========================================
# Unauthorized Access
# =========================================

client = APIClient()

response = client.get("/appointments/mine/")

print("UNAUTHORIZED ACCESS")
print(response.status_code)
print(response.text)
