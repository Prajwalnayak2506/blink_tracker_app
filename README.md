Wellness at Work: Cloud-Synced Eye Tracker
Project Overview
This project is a Full Stack Developer challenge to build a cross-platform (MacOS and Windows) desktop application that tracks eye blinks in real-time. The application integrates a Python-based eye-blink tracker and syncs user data securely to a cloud backend. A web platform provides a read-only dashboard for users to view their blink data. All components are designed with privacy in mind and aim to ensure GDPR compliance.

Features Implemented (Question 1: Cross-Platform Desktop App)
Cross-platform desktop application developed using PyQt5 with a simple, modern black/white/grey GUI.

Login window with user authentication connected to a local backend stub API (no more hardcoded credentials).

Real-time eye blink tracking by running the Python eye-blink tracker script as a subprocess with live blink count display.

Real-time performance monitoring shows CPU usage (%), memory usage (%), and battery percentage.

Fully commented, modular code for easy understanding and extensibility.

How to Run
Start the local backend stub server for login authentication:

bash
python backend_stub.py
Run the main PyQt application:

bash
python main.py
Use the login window to authenticate (test@example.com / 1234).

Upon successful login, the blink tracking and system stats window will open.

GDPR Compliance
Current Measures:
Data Minimization: Only essential personal data (email and blink count) is collected.

Local Prototype: No personal data is permanently stored or shared beyond the local testing environment.

Authentication Stub: Uses a local backend stub with no unencrypted storage of credentials.

Secure Communication (Planned): Future implementation will include HTTPS/TLS for all data transmissions.

Planned Improvements with More Time:
Implement secure, token-based authentication (JWT or OAuth2).

Encrypt user data in transit and at rest on cloud backend (e.g., using AWS RDS encryption).

Develop explicit user consent forms before data collection begins.

Provide users with options to view, export, or delete their data.

Set up automatic data anonymization or deletion policies for inactive accounts.

