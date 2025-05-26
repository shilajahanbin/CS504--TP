from flask import Flask, request, jsonify
from flask_cors import CORS
import random
import time

app = Flask(__name__)
CORS(app)

# Sample user data (can later be replaced with database)
users = {
    "shila": "123456",
    "sara": "abc123"
}

# In-memory OTP storage
otps = {}

# Route for browser testing
@app.route('/')
def home():
    return "✅ MFA Backend is running!"

# Login endpoint
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400

    if username in users and users[username] == password:
        otp = str(random.randint(100000, 999999))
        otps[username] = {
            "otp": otp,
            "expires": time.time() + 300  # expires in 5 minutes
        }
        print(f"[INFO] OTP for {username}: {otp}")
        return jsonify({"message": "OTP sent successfully."}), 200

    return jsonify({"error": "Invalid credentials"}), 401

# OTP verification endpoint
@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.json
    username = data.get("username")
    otp_input = data.get("otp")

    if not username or not otp_input:
        return jsonify({"error": "Missing username or OTP"}), 400

    if username in otps:
        record = otps[username]
        if time.time() > record["expires"]:
            return jsonify({"error": "OTP expired"}), 400
        if otp_input == record["otp"]:
            return jsonify({"message": "Login successful ✅"}), 200
        else:
            return jsonify({"error": "Incorrect OTP"}), 401

    return jsonify({"error": "OTP not found"}), 404

if __name__ == '__main__':
    app.run(debug=True)
