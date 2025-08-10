# ===========================
# A VERY SIMPLE LOGIN SERVER
# ===========================
# This uses Flask (a Python web framework) to create a fake backend
# It only knows ONE valid account: email = test@example.com, password = 1234
# Our PyQt app will send the email + password to this server to check if they match.

from flask import Flask, request, jsonify  # Import tools for web requests/responses

app = Flask(__name__)  # Create the web app

# --------------------------
# 1. Fake "database" of users
# --------------------------
# Just a dictionary where the key = email, value = password
VALID_USERS = {
    "test1@example.com": "1111",   # username: test@example.com, password: 1234
    "test2@example.com": "2222" ,  # username: test@example.com, password: 1234
    "test3@example.com": "3333"  , # username: test@example.com, password: 1234
    "test4@example.com": "4444"   # username: test@example.com, password: 1234
}

# --------------------------
# 2. The /login API endpoint
# --------------------------
@app.route("/login", methods=["POST"])  # This URL accepts POST requests (sending data)
def login():
    # Get the data the user sent from the app as JSON
    data = request.get_json()
    email = data.get("email")        # The email entered by the user
    password = data.get("password")  # The password entered by the user

    # Check if this email exists and the password matches
    if email in VALID_USERS and VALID_USERS[email] == password:
        return jsonify({"success": True, "message": "Login successful"})  # Send success message
    else:
        # If email not found or wrong password, send an error code 401 (unauthorized)
        return jsonify({"success": False, "message": "Invalid email or password"}), 401

# --------------------------
# 3. Start the server
# --------------------------
# Runs locally on "http://127.0.0.1:5000"
if __name__ == "__main__":
    app.run(port=5000)
