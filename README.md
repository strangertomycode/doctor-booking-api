# Doctor Booking API

A REST API for doctor appointment booking, built with Django REST Framework. Supports patient-doctor workflows, rule-based slot generation, and JWT authentication.

**Live API:** https://doctor-booking-api-p9sq.onrender.com  
**Base URL:** `/api/v1/`  
**API Docs:** https://doctor-booking-api-p9sq.onrender.com/api/docs/

---

## Features

**Authentication & Access Control**  
JWT-based authentication with access and refresh tokens. Role-based permissions enforce strict separation between patient and doctor capabilities. Doctor accounts require verification approval before accessing protected endpoints.

**Availability & Scheduling Engine**  
Doctors define weekly availability rules specifying weekday, time window, slot duration, break intervals, and booking horizon. The system automatically generates individual bookable slots from these rules across future dates.

**Appointment System**  
Patients book available slots through a transaction-safe booking flow using `select_for_update` to prevent race-condition double bookings. Appointments follow a lifecycle of pending, completed, and cancelled states with full slot snapshot preservation at booking time.

**Doctor Dashboard & Medical History**  
Doctors access a structured dashboard of scheduled appointments. Verified doctors can retrieve patient medical history through a role-protected endpoint.

---

## Tech Stack

| Layer             | Technology                          |
| ----------------- | ----------------------------------- |
| Framework         | Django, Django REST Framework       |
| Authentication    | SimpleJWT                           |
| Database          | PostgreSQL (Neon)                   |
| API Documentation | drf-spectacular (OpenAPI / Swagger) |
| Static Files      | WhiteNoise                          |
| Server            | Gunicorn                            |
| Containerisation  | Docker                              |
| Hosting           | Render                              |

---

## API Reference

### Authentication

| Method | Endpoint          | Description                      |
| ------ | ----------------- | -------------------------------- |
| POST   | `/auth/register/` | Register as patient or doctor    |
| POST   | `/auth/login/`    | Obtain access and refresh tokens |
| POST   | `/auth/refresh/`  | Refresh access token             |
| GET    | `/auth/me/`       | Retrieve current user details    |

### Availability

| Method | Endpoint                                 | Access  | Description                       |
| ------ | ---------------------------------------- | ------- | --------------------------------- |
| POST   | `/appointments/availability-rules/`      | Doctor  | Create a weekly availability rule |
| GET    | `/appointments/availability-rules/mine/` | Doctor  | List own availability rules       |
| GET    | `/appointments/doctors/<id>/slots/`      | Patient | List available slots for a doctor |

### Appointments

| Method | Endpoint                     | Access  | Description                  |
| ------ | ---------------------------- | ------- | ---------------------------- |
| POST   | `/appointments/`             | Patient | Book an available slot       |
| GET    | `/appointments/mine/`        | Any     | List own appointments        |
| GET    | `/appointments/<id>/`        | Any     | Retrieve appointment details |
| POST   | `/appointments/<id>/cancel/` | Any     | Cancel an appointment        |

### Dashboard & Records

| Method | Endpoint                                       | Access          | Description                    |
| ------ | ---------------------------------------------- | --------------- | ------------------------------ |
| GET    | `/appointments/doctor/dashboard/`              | Doctor          | View scheduled appointments    |
| GET    | `/appointments/patients/<id>/medical-history/` | Verified Doctor | Access patient medical history |

---

## Authentication

All protected endpoints require a JWT access token in the request header:

```
Authorization: Bearer <access_token>
```

---

## Local Setup

**Prerequisites:** Python 3.12+, PostgreSQL, Docker (optional)

### Running with Docker

```bash
git clone https://github.com/strangertomycode/doctor-booking-api
cd doctor-booking-api
cp .env.example .env   # fill in your environment variables
docker compose up --build
```

### Running without Docker

```bash
uv sync
uv run manage.py migrate
uv run manage.py runserver
```

---

## Environment Variables

```env
SECRET_KEY=your_secret_key
DEBUG=False

DB_NAME=your_db_name
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=your_db_host
DB_PORT=5432

ALLOWED_HOSTS=doctor-booking-api-p9sq.onrender.com
```

## Project Structure

```
core/               # Django project settings and root URLs
accounts/           # Custom user model, authentication, doctor profiles
appointments/       # Availability rules, slot generation, appointment logic
Dockerfile
pyproject.toml
uv.lock
```

---

## Deployment

The application is containerised with Docker and deployed on Render. Migrations run automatically on each deploy before the server starts.

```bash
python manage.py migrate --noinput && gunicorn core.wsgi:application --bind 0.0.0.0:$PORT
```
