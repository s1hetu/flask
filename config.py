import os
from dotenv import load_dotenv

load_dotenv()


class BaseConfig:
    SECRET_KEY = os.environ.get("SECRET_KEY")


class Development(BaseConfig):
    DEBUG = True
    POSTGRES_DATABASE = os.environ.get("DB_NAME")
    POSTGRES_PORT = os.environ.get("DB_PORT")
    POSTGRES_USER = os.environ.get("DB_USER")
    POSTGRES_PASSWORD = os.environ.get("DB_PASSWORD")
    POSTGRES_SERVER = "localhost"
    SQLALCHEMY_DATABASE_URI = F"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRES_DATABASE}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = True


class Production(BaseConfig):
    DEBUG = False


app_config = {'dev': Development, 'prod': Production}
