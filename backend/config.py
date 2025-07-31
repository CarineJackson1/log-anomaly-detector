import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configurations for the application
class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///astroskill.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuration classes for different environments
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

class TestingConfig(Config):
    TESTING = True
