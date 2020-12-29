import os
from pathlib import Path

PROJECT_PATH = Path(__file__).resolve().parent

CREDENTIALS_FILE = PROJECT_PATH / "credentials" / "google_creds.json"

CASINO_SCRIPT = PROJECT_PATH / "casino.js"

SELENOID_HOST = "http://46.101.16.210:4444/wd/hub"


class Config:
    DEBUG = False

    # Secret key for session management.
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Disable sorting keys in response.
    JSON_SORT_KEYS = False

    CORS_HEADERS = "Content-Type"

    SHEET_NAME = "Automation BIG Master Roul - Template -ML"


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = False
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
