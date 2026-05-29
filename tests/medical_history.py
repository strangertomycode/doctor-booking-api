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


response = client.get("/appointments/patients/6/medical-history/")

print(response.status_code)
print(response.json())
