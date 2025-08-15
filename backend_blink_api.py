import psycopg2
from psycopg2.extras import RealDictCursor
import os
from flask import Flask, request, jsonify, g
from datetime import datetime

app = Flask(__name__)
DATABASE_URL = os.getenv("DATABASE_URL")  # Should be set in Railway environment variables

def get_db():
    if not hasattr(g, "_database"):
        g._database = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return g._database

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, "_database", None)
    if db is not None:
        db.close()

def create_tables():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id SERIAL PRIMARY KEY,
            email TEXT UNIQUE
        );
        CREATE TABLE IF NOT EXISTS blinks (
            id SERIAL PRIMARY KEY,
            user_id INTEGER REFERENCES users(id),
            blink_count INTEGER,
            timestamp TIMESTAMPTZ
        );
    ''')
    conn.commit()
    cur.close()
    conn.close()

@app.route("/api/blink", methods=["POST"])
def receive_blink_data():
    data = request.get_json()
    user_email = data.get("user_id")  # using user_id as email here
    blink_count = data.get("blink_count")
    timestamp = data.get("timestamp", datetime.utcnow().isoformat())

    if not user_email or blink_count is None:
        return jsonify({"success": False, "message": "Missing required fields"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        INSERT INTO users (email) VALUES (%s)
        ON CONFLICT (email) DO NOTHING
    """, (user_email,))

    cursor.execute("SELECT id FROM users WHERE email = %s", (user_email,))
    user = cursor.fetchone()
    user_id = user["id"]

    cursor.execute("""
        INSERT INTO blinks (user_id, blink_count, timestamp) VALUES (%s, %s, %s)
    """, (user_id, blink_count, timestamp))

    db.commit()
    cursor.close()

    print(f"Received blink data from user {user_email}: {blink_count} at {timestamp}")
    return jsonify({"success": True, "message": "Data received"}), 200

if __name__ == "__main__":
    create_tables()
    port = int(os.getenv("PORT", 5000))  # Use port from env var or 5000
    app.run(host='0.0.0.0', port=port)  # Listen on all interfaces for Railway