# user_model.py
from db import users_collection
from datetime import datetime
import bcrypt

def create_user(username, password, phone):
    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    user = {
        "username": username,
        "password": hashed_pw,
        "phone": phone,
        "last_login": None
    }
    users_collection.insert_one(user)

def get_user_by_username(username):
    return users_collection.find_one({"username": username})

def update_last_login(username):
    users_collection.update_one(
        {"username": username},
        {"$set": {"last_login": datetime.utcnow()}}
    )

def validate_password(input_password, stored_hash):
    return bcrypt.checkpw(input_password.encode('utf-8'), stored_hash)
