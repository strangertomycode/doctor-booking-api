import requests

BASE_URL = "https://doctor-booking-api-0q46.onrender.com/api/v1"


# -----------------------------
# Helpers
# -----------------------------
def print_response(title, response):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print("STATUS:", response.status_code)
    try:
        print(response.json())
    except Exception:
        print(response.text)


# -----------------------------
# 1. Register Users
# -----------------------------
def register_patient():
    return requests.post(
        f"{BASE_URL}/auth/register/",
        json={
            "email": "patient_live@test.com",
            "password": "Test@12345",
            "full_name": "Live Patient",
            "phone_number": "9999999999",
            "role": "patient",
        },
    )


def register_doctor():
    return requests.post(
        f"{BASE_URL}/auth/register/",
        json={
            "email": "doctor_live@test.com",
            "password": "Test@12345",
            "full_name": "Live Doctor",
            "phone_number": "8888888888",
            "role": "doctor",
            "specialization": "Cardiology",
            "qualification": "MBBS",
            "years_of_experience": 5,
            "consultation_fee": "1000.00",
            "hospital_name": "Live Hospital",
            "city": "Kochi",
        },
    )


# -----------------------------
# 2. Login
# -----------------------------
def login(email):
    return requests.post(
        f"{BASE_URL}/auth/login/",
        json={
            "email": email,
            "password": "Test@12345",
        },
    )


# -----------------------------
# 3. Doctor creates availability
# -----------------------------
def create_availability(token):
    return requests.post(
        f"{BASE_URL}/appointments/availability/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "weekday": 5,
            "start_time": "09:00:00",
            "end_time": "13:00:00",
            "slot_duration": 30,
            "break_between_slots": 10,
            "max_days_ahead": 30,
        },
    )


# -----------------------------
# 4. Get slots
# -----------------------------
def get_slots():
    return requests.get(f"{BASE_URL}/appointments/slots/")


# -----------------------------
# 5. Book appointment
# -----------------------------
def book_appointment(token, slot_id):
    return requests.post(
        f"{BASE_URL}/appointments/",
        headers={"Authorization": f"Bearer {token}"},
        json={
            "slot": slot_id,
            "appointment_reason": "Routine checkup",
        },
    )


# -----------------------------
# MAIN FLOW
# -----------------------------
if __name__ == "__main__":
    # 1. Register
    patient_res = register_patient()
    print_response("PATIENT REGISTER", patient_res)

    doctor_res = register_doctor()
    print_response("DOCTOR REGISTER", doctor_res)

    # 2. Login
    patient_login = login("patient_live@test.com")
    print_response("PATIENT LOGIN", patient_login)

    doctor_login = login("doctor_live@test.com")
    print_response("DOCTOR LOGIN", doctor_login)

    patient_token = patient_login.json().get("access")
    doctor_token = doctor_login.json().get("access")

    # 3. Availability
    avail_res = create_availability(doctor_token)
    print_response("CREATE AVAILABILITY", avail_res)

    # 4. Slots
    slots_res = get_slots()
    print_response("LIST SLOTS", slots_res)

    slot_id = None
    try:
        slot_id = slots_res.json()["results"][0]["id"]
    except Exception:
        pass

    # 5. Book appointment
    if slot_id:
        book_res = book_appointment(patient_token, slot_id)
        print_response("BOOK APPOINTMENT", book_res)

    print("\n\nTEST COMPLETED 🚀")
