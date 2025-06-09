# duo_admin.py

from duo_client import Admin
from duo_config import DUO_ADMIN_IKEY, DUO_ADMIN_SKEY, DUO_ADMIN_HOST
import traceback

# ایجاد اتصال به Duo Admin API
admin_api = Admin(
    ikey=DUO_ADMIN_IKEY,
    skey=DUO_ADMIN_SKEY,
    host=DUO_ADMIN_HOST
)

def create_duo_user(username, phone_number):
    try:
        # 1. چک کن آیا یوزر در Duo هست
        users = admin_api.get_users()
        for user in users:
            if user['username'] == username:
                print(f"✔️ Duo user '{username}' already exists.")
                return True

        # 2. ساخت یوزر
        user = admin_api.add_user(username=username)
        user_id = user["user_id"]
        print(f"✅ Duo user created: {username} | ID: {user_id}")

        # 3. چک کن آیا شماره وجود دارد
        phones = admin_api.get_phones()
        for phone in phones:
            if phone['number'] == phone_number:
                phone_id = phone["phone_id"]
                print(f"📱 Existing phone found: {phone_number}")
                break
        else:
            # ساخت شماره جدید
            phone = admin_api.add_phone(number=phone_number, type="Mobile", platform="Google Android")
            phone_id = phone["phone_id"]
            print(f"📱 New phone created: {phone_number}")

        # 4. اتصال شماره به یوزر
        admin_api.add_user_phone(user_id=user_id, phone_id=phone_id)
        print(f"🔗 Phone {phone_number} attached to user {username}")

        return True

    except Exception as e:
        print(f"[!] Failed to create Duo user or attach phone: {e}")
        traceback.print_exc()
        return False
