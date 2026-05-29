from base import APIClient

client = APIClient()


# =========================================
# Register Patient
# =========================================

patient_payload = {
    "email": "patient1@test.com",
    "password": "StrongPassword123",
    "password_confirm": "StrongPassword123",
    "full_name": "Rahul Patient",
    "role": "patient",
    "phone_number": "9999999999",
    "gender": "male",
    "blood_group": "O+",
    "medical_history": "Diabetes",
    "allergies": "Dust allergy",
}

response = client.post(
    "/auth/register/",
    patient_payload,
)

print("PATIENT REGISTER")
print(response.status_code)
print(response.json())
print()


# =========================================
# Register Doctor
# =========================================

doctor_payload = {
    "email": "doctor1@test.com",
    "password": "StrongPassword123",
    "password_confirm": "StrongPassword123",
    "full_name": "Dr Strange",
    "role": "doctor",
    "phone_number": "8888888888",
    "gender": "male",
    "doctor_profile": {
        "specialization": "Cardiology",
        "qualification": "MBBS, MD",
        "years_of_experience": 10,
        "consultation_fee": "1200.00",
        "hospital_name": "Marvel Hospital",
        "city": "Kochi",
        "bio": "Experienced cardiologist",
    },
}

response = client.post(
    "/auth/register/",
    doctor_payload,
)

print("DOCTOR REGISTER")
print(response.status_code)
print(response.json())
