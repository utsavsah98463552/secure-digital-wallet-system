import os
import sys
from flask import Flask, jsonify
from config import config
from database import Database
from services.encryption_service import EncryptionService

def create_app(config_name='development'):
    """Application factory for the Secure Digital Wallet System."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Persistence Layer (Week 2)
    db = Database(app.config['DATABASE_PATH'])
    app.db = db

    # Cryptography Service (Week 3)
    encryption_service = EncryptionService(app.config['ENCRYPTION_KEY'])
    app.encryption_service = encryption_service

    @app.route('/')
    def index():
        return jsonify({
            "system": "Secure Digital Wallet System",
            "status": "online",
            "phase": "Week 3: Security & Cryptography Subsystem Initialized",
            "version": "0.3.0",
            "environment": config_name
        }), 200

    @app.route('/health')
    def health():
        # Verify DB connectivity
        try:
            db.execute_query("SELECT 1")
            db_status = "connected"
        except Exception as e:
            db_status = f"error: {str(e)}"

        # Verify encryption subsystem
        try:
            sample_cipher = encryption_service.encrypt("health_check_payload")
            decrypted = encryption_service.decrypt(sample_cipher)
            crypto_status = "operational" if decrypted == "health_check_payload" else "validation_failed"
        except Exception as e:
            crypto_status = f"error: {str(e)}"

        return jsonify({
            "status": "healthy",
            "database": db_status,
            "cryptography": {
                "algorithm": "Fernet (AES-128-CBC + HMAC-SHA256)",
                "status": crypto_status
            },
            "security": {
                "session_httponly": app.config['SESSION_COOKIE_HTTPONLY'],
                "session_lifetime_sec": app.config['PERMANENT_SESSION_LIFETIME']
            }
        }), 200

    return app

if __name__ == '__main__':
    app = create_app('development')
    print("=" * 60)
    print("Secure Digital Wallet System — Week 3 Security Subsystem")
    print("=" * 60)
    print("Server starting on http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
