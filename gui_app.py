import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
import subprocess
from PyQt5.QtCore import QTimer
import json
import os
import psutil
import requests
from datetime import datetime

CACHE_FILE = "unsent_blinks.json"
# test_data = [
#     {"user_id": "me@example.com", "blink_count": 1, "timestamp": "2025-08-14T10:00:00"},
#     {"user_id": "me@example.com", "blink_count": 2, "timestamp": "2025-08-14T10:00:05"}
# ]

# # save it
# with open(CACHE_FILE, "w") as f:
#     json.dump(test_data, f)

# # read it back
# with open(CACHE_FILE, "r") as f:
#     loaded_data = json.load(f)
# print(loaded_data)
# print(loaded_data)
class BlinkApp(QWidget):
    def __init__(self, user_email):
        super().__init__()
        self.logged_in_user_email = user_email  # Store the email passed at login
        self.setGeometry(100, 100, 300, 200)
        self.setWindowTitle("Blink Counter")

        # Path to blink counter script
        script_path = os.path.join("eye-tracker-share", "eye_blink_counter.py")

        # Start the blink tracker as a subprocess
        self.process = subprocess.Popen(
            [sys.executable, "-u", script_path],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            env=dict(os.environ, PYTHONUNBUFFERED="1")
        )

        # UI Labels
        self.label = QLabel("Blink Count: 0", self)
        self.label.setStyleSheet("font-size: 24px;")
        self.cpu_label = QLabel("CPU: --%", self)
        self.mem_label = QLabel("Memory: --%", self)
        self.battery_label = QLabel("Battery: --%", self)

        # Timers
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_blink_count)
        self.timer.start(500)

        stats_timer = QTimer(self)
        stats_timer.timeout.connect(self.update_system_stats)
        stats_timer.start(1000)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.cpu_label)
        layout.addWidget(self.mem_label)
        layout.addWidget(self.battery_label)
        self.setLayout(layout)
    def add_to_cache(self,user_id,blink_data):
        cache_list = self.load_cached_data()
        data_dict = {"user_id": user_id, "blink_count": blink_data, "timestamp": datetime.utcnow().isoformat()}
        cache_list.append(data_dict)
        self.save_data(cache_list)
        print("[CACHED] Saved blink locally...")
    def load_cached_data(self):
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r") as f: 
                cache_list = json.load(f)
                return cache_list
        else:
            return []
    def save_data(self,cache_list):
        with open(CACHE_FILE,"w") as f:
            json.dump(cache_list,f,indent=2)       
    def try_sending_cache(self):
        cache_list = self.load_cached_data()
        still_unsent = []
        if cache_list:
            for i in cache_list:
                try:
                    response = requests.post(
                        "http://127.0.0.1:5001/api/blink",
                        json={
                            "user_id": i["user_id"],
                            "blink_count": i["blink_count"]
                        },
                        timeout=5
                    )
                    if response.status_code == 200:
                        print(f"[SYNCED] Sent blink_count={i['blink_count']} for user={i['user_id']}")
                    else:
                        still_unsent.append(i)
                except requests.RequestException as e:
                    print(f"[OFFLINE] Could not send to backend: {e}")
                    still_unsent.append(i)  # keep if send failed during exception

            # ✅ Do this AFTER the loop
            if still_unsent:
                self.save_data(still_unsent)
            else:
                if os.path.exists(CACHE_FILE):
                    os.remove(CACHE_FILE)
        else:
            return

    def send_blink_data(self, user_id, blink_count):
        self.try_sending_cache()
        """Send blink data to backend API endpoint."""
        try:
            response = requests.post(
                "http://127.0.0.1:5001/api/blink",
                json={
                    "user_id": user_id,
                    "blink_count": blink_count
                },
                timeout=5
            )
            if response.status_code == 200:
                print(f"[SYNCED] Sent blink_count={blink_count} for user={user_id}")
            else:
                print(f"[ERROR] Server refused blink data: {response.text}")
                self.add_to_cache(user_id, blink_count)
        except requests.RequestException as e:
            print(f"[OFFLINE] Could not send to backend: {e}")
            self.add_to_cache(user_id, blink_count)
    
    def update_system_stats(self):
        """Update CPU, memory, and battery labels."""
        cpu = psutil.cpu_percent()
        mem = psutil.virtual_memory().percent
        battery_info = psutil.sensors_battery()
        battery = battery_info.percent if battery_info else "N/A"

        self.cpu_label.setText(f"CPU: {cpu}%")
        self.mem_label.setText(f"Memory: {mem}%")
        self.battery_label.setText(f"Battery: {battery}%")

    def update_blink_count(self):
        """Read output from blink tracker process and update counter + send to backend."""
        line = self.process.stdout.readline()
        if line.strip():
            try:
                data = json.loads(line)
                blink_count = data.get("blink_count")
                if blink_count is not None:
                    self.label.setText(f"Blink Count: {blink_count}")
                    self.send_blink_data(self.logged_in_user_email, blink_count)
            except json.JSONDecodeError:
                pass  # Ignore invalid JSON


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # For testing: replace with actual email from your login window
    test_email = "test@example.com"
    window = BlinkApp(test_email)
    window.show()

    sys.exit(app.exec_())
