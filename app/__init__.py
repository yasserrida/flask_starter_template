"""Init Flask app"""

import os
from flask import Flask
from flask_cors import CORS
from flask_pymongo import PyMongo
from flask_socketio import SocketIO
from flask_apispec.extension import FlaskApiSpec
from flask_babel import Babel
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from dotenv import load_dotenv
import app.config as conf


load_dotenv(dotenv_path=f"{os.getcwd()}/.env")  # development - testing - production
MODE = os.environ.get("MODE") or "development"


# ------ Init App
app = Flask(__name__)
app.config.from_object(conf.config[MODE])
app.config.update(
    {
        "APISPEC_SPEC": APISpec(
            title="Swagger S4I",
            version="v1",
            plugins=[MarshmallowPlugin()],
            openapi_version="2.0.0",
        ),
        "APISPEC_SWAGGER_URL": "/swagger/",  # URI to access API Doc JSON
        "APISPEC_SWAGGER_UI_URL": "/swagger-ui/",  # URI to access UI of API Doc
    }
)


# ------ Init Modules
CORS(app, resources={r"/": {"origins": "localhost:*"}})
MONGO_DB = PyMongo(app).db
DOCS = FlaskApiSpec(app)
BABEL = Babel(app, locale_selector="en", timezone_selector="UTC+1")
API = Api(app)
SQL_DB = SQLAlchemy(app)
socketio = SocketIO(app)


# ------ Import controllers
from app.models import *
from app.controllers import *

with app.app_context():
    SQL_DB.create_all()
