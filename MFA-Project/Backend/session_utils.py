# session_utils.py
from flask import session
from datetime import datetime, timedelta

def is_session_active(timeout_minutes=5):
    last_active_str = session.get('last_active')
    if not last_active_str:
        return False

    try:
        last_active = datetime.fromisoformat(last_active_str)
    except ValueError:
        return False

    now = datetime.utcnow()
    if now - last_active > timedelta(minutes=timeout_minutes):
        session.clear()
        return False

    session['last_active'] = now.isoformat()
    return True
