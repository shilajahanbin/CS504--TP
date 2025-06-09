# duo_auth.py
import requests
import time
import hmac
import hashlib
import base64
from urllib.parse import urlencode
from duo_config import DUO_IKEY, DUO_SKEY, DUO_HOST

def sign_request(method, host, path, params):
    date = time.strftime('%a, %d %b %Y %H:%M:%S -0000', time.gmtime())
    canon = '\n'.join([date, method.upper(), host.lower(), path, urlencode(params)])
    sig = hmac.new(DUO_SKEY.encode(), canon.encode(), hashlib.sha1).hexdigest()
    auth = f"{DUO_IKEY}:{sig}"
    return {
        "Date": date,
        "Authorization": f"Basic {base64.b64encode(auth.encode()).decode()}",
        "Content-Type": "application/x-www-form-urlencoded"
    }

def verify_duo_otp(username, otp_code):
    path = "/auth/v2/auth"
    method = "POST"
    params = {
        "username": username,
        "factor": "passcode",
        "passcode": otp_code,
        "device": "auto"
    }
    url = f"https://{DUO_HOST}{path}"

    headers = sign_request(method, DUO_HOST, path, params)

    try:
        response = requests.post(url, data=params, headers=headers)
        data = response.json()

        if data.get("stat") == "OK" and data["response"]["result"] == "allow":
            return True
        else:
            print("[!] OTP verification failed:", data)
            return False
    except Exception as e:
        print(f"[!] Exception during OTP verification: {e}")
        return False
