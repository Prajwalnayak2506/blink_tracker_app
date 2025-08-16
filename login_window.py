import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QLineEdit,QPushButton,QMessageBox  # GUI components
import requests
class LoginWindow(QWidget):
    def __init__(self):
        self.on_login_success = None
        super().__init__()
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 300, 150)
        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Enter your email")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.Password)
        login_button = QPushButton("Login")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Email:"))
        layout.addWidget(self.email_input)        
        layout.addWidget(QLabel("Password:"))
        layout.addWidget(self.password_input)
        layout.addWidget(login_button)

        login_button.clicked.connect(self.handle_login)

        self.setLayout(layout)

    def handle_login(self):
        email = self.email_input.text().strip()
        password = self.password_input.text().strip()
        if not email or "@" not in email:
            QMessageBox.warning(self, "Login Failed", "Please enter a valid email address.")
            return
        if not password:
            QMessageBox.warning(self, "Login Failed", "Please enter your password.")
            return
        print(f"Email: {email}, Password: {password}")
        # Step 3: Try to contact the backend server
        try:
            response = requests.post(
                "https://blinktrackerapp-production.up.railway.app/api/users",    # Our local backend server URL
                json={"email": email, "password": password},  # Send data as JSON
                timeout=5  # If server takes >5 seconds, give up
            )

            # Step 4: Handle the server reply
            if response.status_code == 200 and response.json().get("success"):
                # Login OK
                QMessageBox.information(self, "Success", "You have logged in successfully!")
                if self.on_login_success:  # If a success function is set
                    self.on_login_success(email)
                self.close()  # Close login window
            else:
                # Login Failed -> show server's error message
                QMessageBox.warning(self, "Login Failed", response.json().get("message", "Unknown error."))
        
        except requests.RequestException as e:
            # If the server is unreachable or times out
            QMessageBox.critical(self, "Error", f"Could not reach server: {e}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())