from base import APIClient

client = APIClient()


# Patient Login

login_payload = {"email": "patient1@test.com", "password": "StrongPassword123"}

login_response = client.post(
    "/auth/login/",
    login_payload,
)

access = login_response.json()["access"]

client.set_token(access)


# Doctor ID = 2 usually

response = client.get("/appointments/doctors/7/slots/")

print(response.status_code)
print(response.json())
