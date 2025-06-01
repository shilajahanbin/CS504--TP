# duo_routes.py
from flask import Blueprint, request, jsonify
from duo_client import Auth
from duo_config import DUO_IKEY, DUO_SKEY, DUO_HOST
import os
import time
import hmac
import hashlib
import base64
import requests
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

duo_bp = Blueprint('duo', __name__)

# Standard Auth API (SMS)
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

        if response['status'] == 'sent':
            return jsonify({'message': 'SMS passcode sent'}), 200
        else:
            return jsonify({'error': 'Failed to send SMS'}), 401

    except Exception as e:
        return jsonify({'error': f'SMS send error: {str(e)}'}), 500

# OTP verification
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

        if response['result'] == 'allow':
            return jsonify({'message': 'OTP verified'}), 200
        else:
            return jsonify({'error': 'Invalid code'}), 401

    except Exception as e:
        return jsonify({'error': f'OTP verification error: {str(e)}'}), 500

# 🔐 Admin API - Create User in Duo
def create_duo_user(username, phone):
    admin_ikey = os.getenv("DUO_ADMIN_IKEY")
    admin_skey = os.getenv("DUO_ADMIN_SKEY")
    admin_host = os.getenv("DUO_ADMIN_HOST")

    method = 'POST'
    path = '/admin/v1/users'
    host = admin_host
    url = f"https://{host}{path}"
    now = str(int(time.time()))
    params = {
        'username': username
    }

    canon = '\n'.join([now, method, host, path, urlencode(params)])
    sig = hmac.new(admin_skey.encode(), canon.encode(), hashlib.sha1).hexdigest()
    auth = f'Basic {base64.b64encode(f"{admin_ikey}:{sig}".encode()).decode()}'

    headers = {
        'Authorization': auth,
        'Date': time.strftime('%a, %d %b %Y %H:%M:%S UTC', time.gmtime(int(now))),
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        response = requests.post(url, data=params, headers=headers)
        return response.status_code, response.text
    except Exception as e:
        return 500, f'Exception during Duo Admin API request: {str(e)}'
