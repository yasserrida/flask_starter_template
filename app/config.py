"""Config Class"""

import logging
import uuid
import datetime
import os
from dotenv import load_dotenv


load_dotenv(dotenv_path=f"{os.getcwd()}/.env")

logging.basicConfig(
    level=logging.INFO | logging.ERROR,
    filename=f"{os.getcwd()}/log.log",
    format="%(asctime)s %(levelname)s %(message)s",
)


class Configurations: # pylint: disable=too-few-public-methods
    """Configurations Class"""

    # ---------- JWT
    SECRET_KEY = uuid.uuid4().hex
    JWT_SECRET_KEY = uuid.uuid4().hex
    JWT_EXPERATION_DELTA = datetime.timedelta(days=2)


class DevelopmentConfig(Configurations): # pylint: disable=too-few-public-methods
    """Development Configuration Class"""

    DEBUG = os.environ.get("DEBUG") or True
    MONGO_URI = os.environ.get(
        "MONGO_URI") or "mongodb://localhost:27017/se4idata"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or "mysql://root:root@localhost/se4idata"
    )


class TestingConfig(Configurations): # pylint: disable=too-few-public-methods
    """Testing Configuration Class"""

    DEBUG = os.environ.get("DEBUG") or False
    TESTING = os.environ.get("TESTING") or True
    MONGO_URI = os.environ.get(
        "MONGO_URI") or "mongodb://localhost:27017/se4idata"
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get("SQLALCHEMY_DATABASE_URI")
        or "mysql://root:root@localhost:27017/se4idata"
    )


class ProductionConfig(Configurations): # pylint: disable=too-few-public-methods
    """Production Configuration Class"""

    DEBUG = os.environ.get("DEBUG") or False
    MONGO_URI = os.environ.get("MONGO_URI") or ""
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI") or ""


config = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
