from flask import Flask, request, jsonify
from flask_cors import CORS
from duo_client import Auth
from duo_config import DUO_IKEY, DUO_SKEY, DUO_HOST

app = Flask(__name__)
CORS(app)

users = {
    'shila': '123456'
}

@app.route('/')
def index():
    return '<span style="color:green;">✅ MFA Backend is running!</span>'

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if username in users and users[username] == password:
        return jsonify({'message': '✅ Login successful. Proceed to SMS verification'}), 200
    else:
        return jsonify({'error': '❌ Invalid credentials'}), 401

@app.route('/send-sms', methods=['POST'])
def send_sms():
    data = request.get_json()
    username = data.get('username')

    if not username:
        return jsonify({'error': 'Username is required'}), 400

    try:
        duo = Auth(ikey=DUO_IKEY, skey=DUO_SKEY, host=DUO_HOST)
        response = duo.auth(
            factor='sms',
            username=username,
            device='auto'
        )

        if response['status'] == 'sent':
            return jsonify({'message': '✅ SMS passcode sent'}), 200
        else:
            return jsonify({'error': '❌ Failed to send SMS'}), 401

    except Exception as e:
        return jsonify({'error': f'💥 SMS send error: {str(e)}'}), 500

@app.route('/verify-otp', methods=['POST'])
def verify_otp():
    data = request.get_json()
    username = data.get('username')
    code = data.get('code')

    if not username or not code:
        return jsonify({'error': 'Username and code required'}), 400

    try:
        duo = Auth(ikey=DUO_IKEY, skey=DUO_SKEY, host=DUO_HOST)
        response = duo.auth(
            factor='passcode',
            passcode=code,
            username=username
        )

        if response['result'] == 'allow':
            return jsonify({'message': '✅ OTP verified'}), 200
        else:
            return jsonify({'error': '❌ Invalid code'}), 401

    except Exception as e:
        return jsonify({'error': f'💥 Verification error: {str(e)}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
