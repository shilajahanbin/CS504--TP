from flask import Blueprint, request, jsonify, session
from user_model import create_user, get_user_by_username, validate_password, update_last_login
from datetime import datetime
from duo_admin import create_duo_user 

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')
    phone = data.get('phone')

    if get_user_by_username(username):
        return jsonify({'error': 'Username already exists'}), 400

    # Create user in MongoDB
    create_user(username, password, phone)

    # Create user in Duo
    duo_success = create_duo_user(username, phone)
    if not duo_success:
        return jsonify({'error': 'User created in DB but failed to create Duo user'}), 500

    return jsonify({'message': 'User registered successfully'}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    user = get_user_by_username(username)
    if not user or not validate_password(password, user['password']):
        return jsonify({'error': 'Invalid username or password'}), 401

    update_last_login(username)
    session['username'] = username

    return jsonify({'message': 'Login successful, proceed to verify SMS'}), 200
