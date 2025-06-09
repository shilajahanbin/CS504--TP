# duo_routes.py
from flask import Blueprint, request, jsonify
from duo_client import Auth
from duo_config import DUO_IKEY, DUO_SKEY, DUO_HOST

duo_bp = Blueprint('duo', __name__)

@duo_bp.route('/send-sms', methods=['POST'])
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

        if response.get('status') == 'sent':
            return jsonify({'message': 'SMS passcode sent'}), 200
        else:
            return jsonify({'error': 'Failed to send SMS'}), 401

    except Exception as e:
        print(f"[!] Error in Duo SMS: {e}")
        return jsonify({'error': f'SMS send error: {str(e)}'}), 500

@duo_bp.route('/verify-otp', methods=['POST'])
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

        if response.get('result') == 'allow':
            return jsonify({'message': 'OTP verified'}), 200
        else:
            return jsonify({'error': 'Invalid code'}), 401

    except Exception as e:
        print(f"[!] OTP verification error: {e}")
        return jsonify({'error': f'OTP verification error: {str(e)}'}), 500
