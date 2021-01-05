import os
from pathlib import Path
from time import strftime, gmtime

import dotenv

dotenv.load_dotenv()

PROJECT_PATH = Path(__file__).resolve().parent

CREDENTIALS_FILE = PROJECT_PATH / "credentials" / "google_creds.json"
CREDENTIALS_JSON = os.getenv("GOOGLE_CREDENTIALS")

IS_HEROKU = bool(os.getenv("IS_HEROKU"))

CASINO_SCRIPT = PROJECT_PATH / "casino.js"

SELENOID_HOST = "http://46.101.16.210:4444/wd/hub"

LOGGER_PATH = (
    PROJECT_PATH / "logs" / f'consumer_log_{strftime("%Y-%m-%d-%H-%M", gmtime())}.log'
)
LOGGER_FORMAT = (
    "%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s"
)

MRGREEN_EMAIL = os.getenv("MRGREEN_EMAIL")
MRGREEN_PASSWORD = os.getenv("MRGREEN_PASSWORD")


class Config:
    DEBUG = False

    # Secret key for session management.
    SECRET_KEY = os.getenv("SECRET_KEY")

    # Disable sorting keys in response.
    JSON_SORT_KEYS = False

    CORS_HEADERS = "Content-Type"

    SHEET_NAME = {
        "live.grosvenorcasinos.com": "Automation BIG Master Roul - Template -ML",
        "livecasino.mrgreen.com": "Mr,Green BIG Master Roul - Template -ML",
    }


class DevelopmentConfig(Config):
    DEBUG = True


class TestingConfig(Config):
    DEBUG = False
    TESTING = True


class ProductionConfig(Config):
    DEBUG = False


config_by_name = dict(dev=DevelopmentConfig, test=TestingConfig, prod=ProductionConfig)
