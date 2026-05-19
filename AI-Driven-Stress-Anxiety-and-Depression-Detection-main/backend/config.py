import os
from datetime import timedelta

class Config:
    """Base configuration"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # MongoDB Configuration
    MONGODB_SETTINGS = {
        'host': os.environ.get('MONGODB_URI') or 'mongodb+srv://srahulnaik23_db_user:PMhO7Ot7sPKQeJrS@cluster0.mbmv9vm.mongodb.net/mental-health-db?retryWrites=true&w=majority&appName=Cluster0',
        'connect': False  # Lazy connection
    }
    
    # JWT Configuration
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Model Configuration
    MODEL_PATH = os.path.join(os.path.dirname(__file__), 'models', 'distilbert-goemotions-mental')
    
    # CORS Configuration
    CORS_ORIGINS = ['http://localhost:5173', 'http://localhost:3000']

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    TESTING = False

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    TESTING = False

class TestingConfig(Config):
    """Testing configuration"""
    DEBUG = True
    TESTING = True
    MONGODB_SETTINGS = {
        'host': 'mongodb://localhost:27017/test_db',
        'connect': False
    }

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}
