# duo_config.py
import os
from dotenv import load_dotenv

load_dotenv()

# For sending SMS/passcode (Auth API)
DUO_IKEY = os.getenv('DUO_IKEY')
DUO_SKEY = os.getenv('DUO_SKEY')
DUO_HOST = os.getenv('DUO_HOST')

# For managing users via Admin API
DUO_ADMIN_IKEY = os.getenv('DUO_ADMIN_IKEY')
DUO_ADMIN_SKEY = os.getenv('DUO_ADMIN_SKEY')
DUO_ADMIN_HOST = os.getenv('DUO_ADMIN_HOST')
