import jwt
from flask import jsonify, render_template, request, Blueprint
from flask_apispec import doc, use_kwargs, marshal_with
from marshmallow import Schema, fields
from app.config import user_name, password, user_id
from app.config import config
from app import DOCS, app


# just to test, the user and pass should be retrieved from the database and the pass should be encrypted.
users = {user_name: {"user_id": user_id, "password": password}}


class LoginnSchema(Schema):
    """LoginnSchema"""

    username = fields.String(required=True)
    password = fields.String(required=True)


class TokenResponseSchema(Schema):
    """TokenResponseSchema"""

    access_token = fields.String()


class ProtectedResponseSchema(Schema):
    """ProtectedResponseSchema"""

    message = fields.String()


jwt_authentication_bp = Blueprint("jwt_authentication_bp", __name__)


@jwt_authentication_bp.route("/login-form")
def index_jwt():
    """index_jwt"""
    return render_template("jwt_login.html")


@jwt_authentication_bp.route(
    "/jwt-login", methods=["POST"], provide_automatic_options=False
)
@doc(description="Login and get JWT token", tags=["Authentication"])
@use_kwargs(LoginnSchema, location="json")
@marshal_with(TokenResponseSchema())
def login_function(**kwargs):
    """Login and get JWT token"""
    username = kwargs["username"]
    password = kwargs["password"]

    if not username or not password:
        return jsonify({"message": "Missing username or password"}), 400

    if username not in users or users[username]["password"] != password:
        return jsonify({"message": "Invalid username or password"}), 401

    payload = {"user_id": users[username]["user_id"], "username": username}
    token = jwt.encode(payload, config["development"].SECRET_KEY, algorithm="HS256")

    return {"access_token": token}


@jwt_authentication_bp.route(
    "/jwt-protected", methods=["GET"], provide_automatic_options=False
)
@doc(description="Protected resource using JWT token", tags=["Protected"])
@marshal_with(ProtectedResponseSchema())
def protected():
    """Protected resource using JWT token"""
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        key = config["development"].SECRET_KEY
        decoded_token = jwt.decode(token, key, algorithms=["HS256"])
        user_id = decoded_token["user_id"]
        username = decoded_token["username"]

        # Perform any additional authentication or authorization checks based on user_id or username
        if user_id == 1234:
            return {"message": f"Authorized user {username} with ID {user_id}"}
        return {"message": f"Protected resource for user {username} with ID {user_id}"}
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401


# Add the Blueprint to the app and register the API endpoints with Flask-apispec
app.register_blueprint(jwt_authentication_bp, url_prefix="/api")
# DOCS.register(login_function)
# DOCS.register(protected)
