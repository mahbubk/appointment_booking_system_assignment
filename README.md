# Appointment Booking System

A Django-based system to manage healthcare appointments between patients and doctors. This platform supports user
authentication, doctor availability management, appointment scheduling, automated reminders, and monthly reporting.
I Implement here, Backend API only. And I test my app on Linux Environment only.

---

## 📦 Tech Stack

| Layer     | Technology        |
|-----------|-------------------|
| Backend   | Django (Python)   |
| Auth      | JWT via SimpleJWT |
| Database  | PostgreSQL        |
| Scheduler | Celery + Redis    |

---

## 🚀 Features

### ✅ User Types

- **Admin** – Manage all users, appointments, and reports
- **Doctor** – Set time slots, manage appointments, view reports
- **Patient** – Book and manage their appointments

### ✅ Functional Highlights

- User registration & login (with validations)
- Doctor profiles with license, experience, and consultation fee
- Dynamic address selection (Division → District → Thana)
- Appointment booking with time slot validation
- Background tasks for:
    - **Daily appointment reminders**
    - **Monthly report generation**
- Filtering for appointments and doctors

---

## ⚙️ Setup Instructions

### 1. Clone & Create Virtual Environment

    git clone https://github.com/your-username/appointment-booking-system.git
    cd appointment-booking-system

    python -m venv venv
    source venv/bin/activate

### 2. Install Requirements

    pip install -r requirements.txt

### 3. Setup Database

Create your database in PostgreSQL first, then run:

    python manage.py makemigrations
    python manage.py migrate

### 4. Seed Sample Data

    python manage.py loaddata seed_data.json

### 5. Run Development Server

    python manage.py runserver

### 6. Installed Redis (Linux/Debian)

    sudo apt install redis-server
    sudo apt update
    redis-server --version

---

## 🔐 Authentication (JWT)

- Login: `POST /api/v1/user/login/` → Returns access & refresh tokens
- Include access token in header for authenticated requests:

  Authorization: Bearer <access_token>

---

## 📤 API Overview (Examples)

| Endpoint                | Method | Description                                |
|-------------------------|--------|--------------------------------------------|
| `v1/`                   | GET    | Full API docs   Swagger UI                 
 `api/v1/user/login/`    | 	POST	 | Get new access token & refresh token token |
 `api/v1/refresh/token/` | 	POST	 | Get new access token using refresh token   

*(Full API docs available in Swagger UI)*




---

## 🧪 Validation Logic

- 📱 Phone: Must begin with `+88` and be exactly 14 digits
- 📧 Email & phone must be unique
- 🔐 Password: Min 8 characters, 1 uppercase, 1 digit, 1 special character
- 📅 Appointment time: Must fall within doctor’s available slots
- 🖼 File uploads: JPEG/PNG only, max size 5MB

---

## 🕓 Background Jobs

---





---

| Task                 | Schedule           | Description                      |
|----------------------|--------------------|----------------------------------|
| Appointment Reminder | Daily (via Celery) | Sends reminder 24 hours before   |
| Monthly Report       | 1st of every month | Summarizes appointments/earnings |

To run:

    celery -A appointment_booking_system worker --loglevel=info
    celery -A appointment_booking_system beat --loglevel=info

---

## 📄 Database Schema (Simplified)

- **User** – Base user with role, contact, and address
- **DoctorProfile** – 1:1 with User; includes license, specialization, etc.
- **TimeSlot** – Weekly availability per doctor
- **Appointment** – Booking data with date, time, notes, status
- **MonthlyReport** – Auto-generated summary (per doctor/month)
- **AppointmentReminder** – Tracks if reminders have been sent

---

## 🧪 Sample Data

Loaded via `seed_data.json`, includes:

- 30 users (10 doctors, 10 patients)
- 15 doctor profiles
- 10+ time slots
- 10 appointments
- 5 monthly reports
- 5 appointment reminders

---

## 🧩 Challenges & Assumptions

- Dynamic address selection via foreign key (Division > District > Thana)
- Time slot conflict detection to ensure valid bookings
- Passwords securely hashed; JWT tokens managed via SimpleJWT
- Scheduler assumed to run locally (Redis + Celery setup provided)

---

## 📁 Project Outcome

- [x] Django-based backend with JWT auth
- [x] Role-based permissions
- [x] Complete appointment booking workflow
- [x] Reminder system & monthly reports
- [x] Swagger/Postman API docs
- [x] Implement Centralized Logging System  (For better performance tracking & monitoring)
- [x] `.env`, `requirements.txt`, and `seed_data.json`

## Admin User email & Password

- email - admin@example.com
- password - Admin.1234


