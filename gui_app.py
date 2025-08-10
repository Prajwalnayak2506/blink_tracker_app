import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout  # GUI components
import subprocess #this module to to let this file run another file in the background and then use its output for modifying things in this file
from PyQt5.QtCore import QTimer
import json
import os
import psutil

class BlinkApp(QWidget):
    def __init__(self):
        super().__init__() 
        self.setGeometry(100, 100, 300, 200)
        self.process = subprocess.Popen([sys.executable, "-u", "eye-tracker-share\\eye_blink_counter.py"],    stdout=subprocess.PIPE,    stderr=subprocess.PIPE,    text=True,    bufsize=1,    env=dict(os.environ, PYTHONUNBUFFERED="1"))#bufsize=1 meaning one line once and self.process allows other methods in yuor clas to access the running process
        self.setWindowTitle("Blink Counter")
        # self.setGeometry(100, 100, 300, 100)# x, y, width, height
        self.label = QLabel("Blink Count: 0", self) 
        self.label.setStyleSheet("font-size: 24px;")
        self.cpu_label = QLabel("CPU: --%", self)
        self.mem_label = QLabel("Memory: --%", self)
        self.battery_label = QLabel("Battery: --%", self)
        self.timer = QTimer(self) #creatign the timer 
        self.timer.timeout.connect(self.update_blink_count)
        self.timer.start(500)
        stats_timer = QTimer(self)
        stats_timer.timeout.connect(self.update_system_stats)
        stats_timer.start(1000)  # 1 second refresh
        layout = QVBoxLayout()#Vertical layout (top to bottom)
        layout.addWidget(self.label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.mem_label)
        layout.addWidget(self.battery_label) 
        self.setLayout(layout)
    def update_system_stats(self):
       cpu = psutil.cpu_percent()
       vm = psutil.virtual_memory().percent
       battery = psutil.sensors_battery()
       battery_info = psutil.sensors_battery()
       battery = battery_info.percent if battery_info else "N/A"
       self.cpu_label.setText(f"CPU: {cpu}%")
       self.mem_label.setText(f"Memory: {vm}%")
       self.battery_label.setText(f"Battery: {battery}%")
    def update_blink_count(self):
        line = self.process.stdout.readline()
        # print(line)
        if line.strip():  # Only if the line has actual content
         try:
            data = json.loads(line)
            blink_count = data.get("blink_count")
            # print("Raw line:",blink_count)
            if blink_count is not None:
                self.label.setText(f"Blink Count: {blink_count}")
         except json.JSONDecodeError:
            pass  # Ignore lines that aren’t valid JSON
if __name__ == '__main__':
    app = QApplication(sys.argv)  
    window = BlinkApp()
    window.show()                
    sys.exit(app.exec_())