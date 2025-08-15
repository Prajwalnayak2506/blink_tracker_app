import requests

data = {
    "user_id": "testuser@example.com",
    "blink_count": 10,
    "timestamp": "2025-08-16T00:00:00"
}

url = "https://blinktrackerapp-production.up.railway.app/api/blink"  # Your Railway backend URL

response = requests.post(url, json=data)
print(response.status_code)
print(response.json())
