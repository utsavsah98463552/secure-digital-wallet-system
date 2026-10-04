import os
from cryptography.fernet import Fernet

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(32).hex()
    DATABASE_PATH = os.environ.get('DATABASE_PATH') or 'ewallet.db'
    ENCRYPTION_KEY = os.environ.get('ENCRYPTION_KEY') or Fernet.generate_key()
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    PERMANENT_SESSION_LIFETIME = 1800  # 30 minutes

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):
    """Development environment configuration."""
    DEBUG = True
    SESSION_COOKIE_SECURE = False

class TestingConfig(Config):
    """Testing environment configuration."""
    TESTING = True
    DEBUG = True
    DATABASE_PATH = ':memory:'
    SESSION_COOKIE_SECURE = False

class ProductionConfig(Config):
    """Production environment configuration."""
    DEBUG = False
    SESSION_COOKIE_SECURE = True

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
