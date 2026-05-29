import os

scripts = [
    "register_users.py",
    "login.py",
    "doctor_create_availability.py",
    "list_doctor_slots.py",
    "book_appointment.py",
    "my_appointments.py",
    "doctor_dashboard.py",
    "update_appointment_status.py",
    "medical_history.py",
    "negative_tests.py",
    "cancel_appointment.py",
]

for script in scripts:
    print()
    print("=" * 60)
    print(f"RUNNING: {script}")
    print("=" * 60)
    print()

    os.system(f"python3 {script}")
