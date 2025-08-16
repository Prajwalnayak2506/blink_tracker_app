import requests

# 1. Test login endpoint
login_url = "https://blinktrackerapp-production.up.railway.app/users"  # Use /users if that's your route
login_payload = {
    "email": "test1@example.com",
    "password": "1111"
}
login_response = requests.post(login_url, json=login_payload)
print("Login Status:", login_response.status_code)
print("Login Response:", login_response.text)

# 2. Test blink data endpoint
blink_url = "https://blinktrackerapp-production.up.railway.app/api/blink"
blink_payload = {
    "user_id": "test1@example.com",
    "blink_count": 5,
    "timestamp": "2025-08-16T20:25:00"
}
blink_response = requests.post(blink_url, json=blink_payload)
print("Blink Status:", blink_response.status_code)
print("Blink Response:", blink_response.text)
