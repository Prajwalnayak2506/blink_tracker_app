import sys
from PyQt5.QtWidgets import QApplication
from login_window import LoginWindow
from gui_app import BlinkApp

def main():
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    def open_blink_app(user_email):
        login_window.close()
        blink_app = BlinkApp(user_email)
        blink_app.show()
        app.blink_app = blink_app  
    login_window.on_login_success = open_blink_app
    login_window.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()
