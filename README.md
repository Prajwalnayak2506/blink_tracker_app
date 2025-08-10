# Wellness at Work: Cloud-Synced Eye Tracker

## Project Overview

This project is a Full Stack Developer challenge to build a cross-platform (MacOS and Windows) desktop application that tracks eye blinks in real-time. The application integrates a Python-based eye-blink tracker and syncs user data securely to a cloud backend. A web platform provides a read-only dashboard for users to view their blink data. All components are designed with privacy in mind and aim to ensure GDPR compliance.

---

## Features Implemented (Question 1: Cross-Platform Desktop App)

- **Cross-platform desktop application** developed using PyQt5 with a simple, modern black/white/grey GUI.
- **Login window** with user authentication connected to a local backend stub API (no more hardcoded credentials).
- **Real-time eye blink tracking** by running the Python eye-blink tracker script as a subprocess with live blink count display.
- **Real-time performance monitoring**: CPU usage (%), memory usage (%), and battery percentage.
- **Fully commented, modular code** for easy understanding and extensibility.

---

## How to Run

1. **Start the local backend stub server** for login authentication:  python backend_stub.py
2. **Run the main PyQt application**: python main.py
3. **Login credentials for testing**:
Email: test1@example.com
Password: 1111


Upon successful login, the blink tracking and system stats window will open.

---

## GDPR Compliance

### Current Measures:
- **Data Minimization:** Only essential personal data (email and blink count) is collected.
- **Local Prototype:** No personal data is permanently stored or shared beyond the local testing environment.
- **Authentication Stub:** Uses a local backend stub with no unencrypted storage of credentials.
- **Secure Communication (Planned):** Future implementation will include HTTPS/TLS for all data transmissions.

### Planned Improvements with More Time:
- Implement secure, token-based authentication (JWT or OAuth2).
- Encrypt user data in transit and at rest on cloud backend (e.g., using AWS RDS encryption).
- Develop explicit user consent forms before data collection begins.
- Provide users with options to view, export, or delete their data.
- Set up automatic data anonymization or deletion policies for inactive accounts.

---

## Architecture Diagram

Below is a high-level architecture diagram showing how the components interact:
+---------------------+ +--------------------+ +---------------------+
| | | | | |
| Cross-Platform | | Cloud Backend & | | WaW Web Platform |
| Desktop Application | <---> | Database (AWS) | <---> | Read-Only Dashboard |
| (PyQt5, Blink Tracker| | (API, S3, RDS) | | (Web Framework) |
| Subprocess, UI) | | | | |
+---------------------+ +--------------------+ +---------------------+

User authenticates on the desktop app.

Blink data is collected and sent securely to the backend.

Backend stores user and blink data.

Web platform fetches data via secure API to display to users.

---

## Next Steps

- Build and deploy the cloud backend using AWS services (S3, RDS).
- Develop secure APIs for syncing blink data and user authentication.
- Create the WaW web platform dashboard to visualize user data securely.
- Implement CI/CD pipelines with automated testing.
- Enhance application with performance optimizations and notifications.

---




