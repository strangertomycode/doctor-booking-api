import os

scripts = [
    "tests/register_users.py",
    "tests/login.py",
    "tests/doctor_create_availability.py",
    "tests/list_doctor_slots.py",
    "tests/book_appointment.py",
    "tests/my_appointments.py",
    "tests/doctor_dashboard.py",
    "tests/update_appointment_status.py",
    "tests/medical_history.py",
    "tests/negative_tests.py",
    "tests/cancel_appointment.py",
]

for script in scripts:
    print()
    print("=" * 60)
    print(f"RUNNING: {script}")
    print("=" * 60)
    print()

    os.system(f"python3 {script}")
