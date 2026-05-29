from base import APIClient

client = APIClient()


# Login as Patient

login_payload = {"email": "patient1@test.com", "password": "StrongPassword123"}

login_response = client.post(
    "/auth/login/",
    login_payload,
)

access = login_response.json()["access"]

client.set_token(access)


payload = {"cancellation_reason": "Emergency"}

response = client.post(
    "/appointments/3/cancel/",
    payload,
)

print(response.status_code)
print(response.json())
