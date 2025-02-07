# coding=utf-8
import datetime
import os

from dotenv import load_dotenv, find_dotenv

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)
LOCAL_ENV_FILE = find_dotenv(".env.local")
if LOCAL_ENV_FILE:
    load_dotenv(LOCAL_ENV_FILE)


class Config(object):
    """
    Initial Configurations for the Flask App
    """

    CSRF_ENABLED = True
    DEBUG = False

    SECRET_KEY = os.environ.get(
        "SECRET_KEY",
        "HACKATHON_SECRET_KEY_TODO_INSERT",
    )
    expires = datetime.timedelta(days=30)

    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DB")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    CELERY_CONFIG = {
        "CELERY_BROKER_URL": "redis://localhost:6379/0",
        "CELERY_RESULT_BACKEND": "redis://localhost:6379/0",
        "CELERY_TASK_SERIALIZER": "json",
        "CELERYD_POOL": 4,
        "BROKER_HEARTBEAT": 0,
        "BROKER_CONNECTION_MAX_RETRIES": None,
        "BROKER_POOL_LIMIT": None,
        "CELERY_IGNORE_RESULT": True,
        "CELERY_UTC_ENABLE": True,
    }
    MAIL_SERVER = 'smtp.office365.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_PASSWORD = 'internbuddy!'
    MAIL_USERNAME = 'alexainternbuddy@outlook.com'  # enter your email here
    MAIL_DEFAULT_SENDER = 'alexainternbuddy@outlook.com' # enter your email here

    CELERY_UTC_ENABLE = True
    SQLALCHEMY_POOL_TIMEOUT = None
    STATIC_FOLDER = os.path.join(basedir, "frontend", "public/")
    UPLOAD_FOLDER = os.path.join(basedir, "tmp", "upload/")
    ZIP_FOLDER = os.path.join(basedir, "tmp", "zipped_tmp")
    PRODUCTION = False


class DevelopmentConfig(Config):
    """
    Developmental Configurations
    """

    DEBUG = True
    LOCALE_DEFAULT = "en_US"
    SQLALCHEMY_DATABASE_URI = "sqlite:///hackathon-alexa-db.db"


class ProductionConfig(Config):
    """
    Production Configurations
    """

    PRODUCTION = True
    DEBUG = False
    LOCALE_DEFAULT = "en_US.utf8"
    JWT_COOKIE_SECURE = True


class TestingConfig(Config):
    """
    Testing Configurations
    """

    TESTING = True
    CSRF_ENABLED = False
    SQLALCHEMY_DATABASE_URI = "sqlite://"


config = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
