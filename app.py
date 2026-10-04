import os
import sys
from flask import Flask, jsonify
from config import config
from database import Database

def create_app(config_name='development'):
    """Application factory for the Secure Digital Wallet System."""
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    # Initialize Persistence Layer (Week 2)
    db = Database(app.config['DATABASE_PATH'])
    app.db = db

    @app.route('/')
    def index():
        return jsonify({
            "system": "Secure Digital Wallet System",
            "status": "online",
            "phase": "Week 2: Database Layer Initialized",
            "version": "0.2.0",
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

        return jsonify({
            "status": "healthy",
            "database": db_status,
            "security": {
                "session_httponly": app.config['SESSION_COOKIE_HTTPONLY'],
                "session_lifetime_sec": app.config['PERMANENT_SESSION_LIFETIME']
            }
        }), 200

    return app

if __name__ == '__main__':
    app = create_app('development')
    print("=" * 60)
    print("Secure Digital Wallet System — Week 2 Database Layer")
    print("=" * 60)
    print("Server starting on http://127.0.0.1:5000")
    print("Press CTRL+C to quit")
    print("=" * 60)
    app.run(debug=True, host='127.0.0.1', port=5000)
