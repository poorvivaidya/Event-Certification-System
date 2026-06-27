# 🎓 Event Lifecycle & Certification System

A full-stack Django-based Event Lifecycle & Certification System that streamlines the complete event management process—from student registration to certificate generation and verification.

The system enables secure participant registration, transaction verification, attendance management, feedback collection, automated PDF certificate generation, QR-based certificate verification, and role-based access for students and administrators.

---

## 🚀 Features

### 👨‍🎓 Student Module

- Student Sign Up & Login
- Secure authentication
- Forgot Password (Email Reset)
- Register for multiple events
- Event selection from Upcoming Events
- Dashboard displaying all registered events
- Upload payment receipt
- Unique transaction ID validation
- Student ID format validation
- Feedback submission
- Certificate download
- QR-code verified certificates
- Remember Me login option

---

### 👨‍💼 Admin Module

- Secure Django Administration
- Create and manage events
- Verify payment transactions
- Mark attendance
- View all participants
- Manage multiple event registrations
- Bulk participant upload via CSV
- Assign certificate types:
  - Participation
  - First Place 🥇
  - Second Place 🥈
  - Third Place 🥉
- Automatic certificate generation
- View participant details

---

## 🏆 Certificate Features

- Professional PDF certificate
- QR Code Verification
- Unique Certificate ID
- Student ID
- Event Details
- Date of Event
- Digital Signature
- Authorised Signatory
- Winner Certificates
- Participation Certificates
- Certificate Verification Page

---

## 🔐 Authentication

- Student Registration
- Student Login
- Logout
- Forgot Password
- Password Reset via Email
- Django Admin Authentication

---

## 📧 Email Features

- Registration Confirmation Email
- Password Reset Email
- Secure SMTP Integration

---

## 📱 Responsive UI

- Bootstrap 5
- Mobile Friendly
- Responsive Dashboard
- Modern Login Screens
- Professional Certificate Design

---

## 🛠️ Technology Stack

### Backend

- Django 5
- Python 3

### Frontend

- HTML5
- CSS3
- Bootstrap 5
- JavaScript

### Database

- SQLite (Development)
- PostgreSQL (Production - Render)

### Libraries

- ReportLab
- QRCode
- Pillow
- WhiteNoise
- Gunicorn

---

## 📂 Project Structure

```
event_cert/
│
├── event_cert/
│
├── events/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   ├── admin.py
│   ├── utils.py
│   ├── validators.py
│
├── media/
│
├── static/
│   ├── css/
│   ├── js/
│   ├── images/
│
├── templates/
│
├── requirements.txt
│
├── manage.py
```

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/poorvivaidya/Event-Certification-System.git
```

Move into the project

```bash
cd YOUR_REPOSITORY
```

Create virtual environment

```bash
python -m venv venv
```

Activate virtual environment

Windows

```bash
venv\Scripts\activate
```

Linux / Mac

```bash
source venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

Run the server

```bash
python manage.py runserver
```

---

## 🔑 Environment Variables

Create a `.env` file

```
SECRET_KEY=your_secret_key

DEBUG=False

EMAIL_HOST_USER=eventcertsystem@gmail.com

EMAIL_HOST_PASSWORD=fwyl mktj ltzd horu
```

---

## 📷 Key Modules

- Student Registration
- Event Registration
- Transaction Verification
- Attendance Tracking
- Feedback Management
- Certificate Generation
- QR Verification
- Password Reset
- Django Administration

---

## 🔍 Certificate Verification

Every certificate contains

- QR Code
- Certificate ID
- Verification URL

The QR code redirects to the verification page where the certificate authenticity can be verified.

---

## 🌐 Live Application

**Live Demo:** https://event-certification-system-1.onrender.com

Experience the complete Event Lifecycle & Certification System, including student registration, event management, certificate generation, and QR-based certificate verification.

## 📌 Future Enhancements

- Email certificate after event completion
- Event analytics dashboard
- Multiple admin roles
- Online payment gateway integration
- Event reminders
- Certificate templates
- Cloud storage for certificates
- Attendance via QR scanning

---

## 👩‍💻 Developed By

**Poorvi Vaidya**

Computer Science & Engineering

SJB Institute of Technology

---

## 📄 License

This project is developed for academic and learning purposes.