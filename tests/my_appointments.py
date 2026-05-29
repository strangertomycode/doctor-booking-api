from base import APIClient

client = APIClient()


# Login

login_payload = {"email": "patient1@test.com", "password": "StrongPassword123"}

login_response = client.post(
    "/auth/login/",
    login_payload,
)

access = login_response.json()["access"]

client.set_token(access)


response = client.get("/appointments/mine/")

print(response.status_code)
print(response.json())
