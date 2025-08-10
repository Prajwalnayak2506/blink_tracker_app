import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout,QLineEdit,QPushButton  # GUI components
class LoginWindow(QWidget):
    def __init__(self):
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
        email = self.email_input.text()
        password = self.password_input.text()
        print(f"Email: {email}, Password: {password}")
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())

        



