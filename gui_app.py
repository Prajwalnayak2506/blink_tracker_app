import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout  # GUI components
import subprocess #this module to to let this file run another file in the background and then use its output for modifying things in this file

class BlinkApp(QWidget):
    def __init__(self):
        super().__init__() 
        result = subprocess.Popen(["python", "eye-tracker-share\eye_blink_counter.py"],stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)#bufsize=1 meaning one line once
        self.setWindowTitle("Blink Counter")
        self.setGeometry(100, 100, 300, 100)# x, y, width, height
        self.label = QLabel("Blink Count: 0", self) 
        self.label.setStyleSheet("font-size: 24px;")
        layout = QVBoxLayout()#Vertical layout (top to bottom)
        layout.addWidget(self.label) 
        self.setLayout(layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)  
    window = BlinkApp()
    window.show()                
    sys.exit(app.exec_())