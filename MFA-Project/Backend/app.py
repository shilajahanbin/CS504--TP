# app.py
from flask import Flask
from flask_cors import CORS
from auth_routes import auth_bp
from duo_routes import duo_bp
from dotenv import load_dotenv
import os

load_dotenv()
app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "dev_key")
CORS(app)

app.register_blueprint(auth_bp)
app.register_blueprint(duo_bp)

@app.route('/')
def index():
    return '<span style="color:green;">✅ MFA Backend is running!</span>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
