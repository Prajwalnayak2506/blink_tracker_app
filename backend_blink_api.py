from flask import Flask, request, jsonify
from datetime import datetime

app = Flask(__name__)

# A simple in-memory store for received blink data (for demo only)
blink_data_store = {}

@app.route("/api/blink", methods=["POST"])
def receive_blink_data():
    data = request.get_json()
    user_id = data.get("user_id")
    blink_count = data.get("blink_count")
    timestamp = data.get("timestamp", datetime.utcnow().isoformat())  # Optional; use current time if missing

    if not user_id or blink_count is None:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    # Store the received data; here we append to a list per user
    if user_id not in blink_data_store:
        blink_data_store[user_id] = []
    blink_data_store[user_id].append({"blink_count": blink_count, "timestamp": timestamp})

    print(f"Received blink data from user {user_id}: {blink_count} at {timestamp}")
    return jsonify({"success": True, "message": "Data received"}), 200

if __name__ == "__main__":
    app.run(port=5001)  # Run on port 5001 to avoid conflict with login server
