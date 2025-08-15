import sqlite3
from flask import Flask, request, jsonify, g
from datetime import datetime

app = Flask(__name__)

# One-time DB/table creation on startup
with sqlite3.connect('blinks.db') as conn:
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS blinks (
            user_id TEXT,
            blink_count INTEGER,
            timestamp TEXT
        )
    ''')
    conn.commit()

DATABASE = 'blinks.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route("/api/blink", methods=["POST"])
def receive_blink_data():
    data = request.get_json()
    user_id = data.get("user_id")
    blink_count = data.get("blink_count")
    timestamp = data.get("timestamp", datetime.utcnow().isoformat())

    if not user_id or blink_count is None:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    db = get_db()
    cursor = db.cursor()
    cursor.execute(
        "INSERT INTO blinks (user_id, blink_count, timestamp) VALUES (?, ?, ?)",
        (user_id, blink_count, timestamp)
    )
    db.commit()

    print(f"Received blink data from user {user_id}: {blink_count} at {timestamp}")
    return jsonify({"success": True, "message": "Data received"}), 200

if __name__ == "__main__":
    app.run(port=5001)
