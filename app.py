import os
import sys
from flask import Flask, jsonify
from config import config

def create_app(config_name='development'):
    """Application factory for the Secure Digital Wallet System."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    @app.route('/')
    def index():
        return jsonify({
            "system": "Secure Digital Wallet System",
            "status": "online",
            "phase": "Week 1: Architecture & Foundation Initialized",
            "version": "0.1.0",
            "environment": config_name
        }), 200

    @app.route('/health')
    def health():
        return jsonify({
            "status": "healthy",
            "security": {
                "session_httponly": app.config['SESSION_COOKIE_HTTPONLY'],
                "session_lifetime_sec": app.config['PERMANENT_SESSION_LIFETIME']
            }
        }), 200

    return app

if __name__ == '__main__':
    app = create_app('development')
    print("=" * 60)
    print("Secure Digital Wallet System — Week 1 Bootstrap")
    print("=" * 60)
    print("Server starting on http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
