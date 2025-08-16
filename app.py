from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DATABASE_URL = os.getenv("DATABASE_URL")

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
def blink():
    data = request.get_json()
    email = data.get("user_id")
    blink_count = data.get("blink_count")
    timestamp = data.get("timestamp")

    if email is None or blink_count is None or timestamp is None:
        return jsonify({"success": False, "message": "Missing fields"}), 400

    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()
    cur.execute("INSERT INTO users (email) VALUES (%s) ON CONFLICT (email) DO NOTHING", (email,))
    cur.execute("SELECT id FROM users WHERE email=%s", (email,))
    user_id = cur.fetchone()[0]
    cur.execute("INSERT INTO blinks (user_id, blink_count, timestamp) VALUES (%s, %s, %s)", (user_id, blink_count, timestamp))
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"success": True})

if __name__ == "__main__":
    create_tables()
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
