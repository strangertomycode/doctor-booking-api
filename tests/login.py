from base import APIClient

client = APIClient()

payload = {"email": "patient1@test.com", "password": "StrongPassword123"}

response = client.post(
    "/auth/login/",
    payload,
)

print(response.status_code)
print(response.json())
