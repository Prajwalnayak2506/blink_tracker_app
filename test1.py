import requests

url = "https://blinktrackerapp-production.up.railway.app/users"
payload = {"email": "test1@example.com", "password": "1111"}
r = requests.post(url, json=payload)
print(r.status_code, r.text)
