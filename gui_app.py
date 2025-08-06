import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout  # GUI components
import subprocess #this module to to let this file run another file in the background and then use its output for modifying things in this file
from PyQt5.QtCore import QTimer
import json
import os
class BlinkApp(QWidget):
    def __init__(self):
        super().__init__() 
        self.process = subprocess.Popen([sys.executable, "-u", "eye-tracker-share\\eye_blink_counter.py"],    stdout=subprocess.PIPE,    stderr=subprocess.PIPE,    text=True,    bufsize=1,    env=dict(os.environ, PYTHONUNBUFFERED="1"))#bufsize=1 meaning one line once and self.process allows other methods in yuor clas to access the running process
        self.setWindowTitle("Blink Counter")
        self.setGeometry(100, 100, 300, 100)# x, y, width, height
        self.label = QLabel("Blink Count: 0", self) 
        self.label.setStyleSheet("font-size: 24px;")
        self.timer = QTimer(self) #creatign the timer 
        self.timer.timeout.connect(self.update_blink_count)
        self.timer.start(500)
        layout = QVBoxLayout()#Vertical layout (top to bottom)
        layout.addWidget(self.label) 
        self.setLayout(layout)
    def update_blink_count(self):
        line = self.process.stdout.readline()
        print(line)
        if line.strip():  # Only if the line has actual content
         try:
            data = json.loads(line)
            blink_count = data.get("blink_count")
            print("Raw line:",blink_count)
            if blink_count is not None:
                self.label.setText(f"Blink Count: {blink_count}")
         except json.JSONDecodeError:
            pass  # Ignore lines that aren’t valid JSON
if __name__ == '__main__':
    app = QApplication(sys.argv)  
    window = BlinkApp()
    window.show()                
    sys.exit(app.exec_())