from duo_client import Admin
import os
import traceback
from dotenv import load_dotenv

load_dotenv()

DUO_ADMIN_IKEY = os.getenv("DUO_ADMIN_IKEY")
DUO_ADMIN_SKEY = os.getenv("DUO_ADMIN_SKEY")
DUO_ADMIN_HOST = os.getenv("DUO_ADMIN_HOST")

admin_api = Admin(
    ikey=DUO_ADMIN_IKEY,
    skey=DUO_ADMIN_SKEY,
    host=DUO_ADMIN_HOST
)

def create_duo_user(username, phone_number):
    try:
        # check if user already exists
        users = admin_api.get_users()
        for user in users:
            if user['username'] == username:
                print(f"[!] Duo user '{username}' already exists.")
                return True  # Consider it successful since user is already created

        # 1. Create Duo user
        user = admin_api.add_user(username=username)
        user_id = user["user_id"]

        # check if phone already exists
        phones = admin_api.get_phones()
        for phone in phones:
            if phone['number'] == phone_number:
                phone_id = phone['phone_id']
                break
        else:
            # 2. Add phone device
            phone = admin_api.add_phone(number=phone_number, type="Mobile", platform="Google Android")
            phone_id = phone["phone_id"]

        # 3. Associate phone with user
        admin_api.add_user_phone(user_id=user_id, phone_id=phone_id)

        print(f"[+] Duo user created and phone attached: {username}")
        return True
    except Exception as e:
        print(f"[!] Failed to create Duo user or attach phone: {e}")
        traceback.print_exc()
        return False
