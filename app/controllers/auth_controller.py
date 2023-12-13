""" Auth Controller """

import jwt
from flask import session, jsonify, render_template, request, Blueprint
from flask_apispec import doc, use_kwargs, marshal_with
from app.config import config
from app.models.auth import LoginSchema, TokenResponseSchema, ProtectedResponseSchema
from app import MONGO_DB as DB, DOCS, app

jwt_auth_bp = Blueprint(
    "jwt_auth_bp", __name__, template_folder="templates", static_folder="static"
)


@jwt_auth_bp.route("", methods=["GET"], provide_automatic_options=False)
@doc(description="Get Login form", tags=["Authentication"])
def index():
    """index login form"""
    return render_template("login.html")


@jwt_auth_bp.route("", methods=["POST"], provide_automatic_options=False)
@doc(description="Login and get JWT token", tags=["Authentication"])
@use_kwargs(LoginSchema, location="json")
@marshal_with(TokenResponseSchema())
def login(**kwargs):
    """Login and get JWT token
    Returns:
        flask.Response
    """
    email = kwargs["email"]
    password = kwargs["password"]

    if not email or not password:
        return jsonify({"message": "Missing email or password"}), 400

    user = DB.users.find_one({"email": email, "password": password})  # type: ignore
    if not user:
        return jsonify({"message": "Invalid email or password"}), 401

    session["username"] = f"{user['first_name']} {user['last_name']}"
    token = jwt.encode(
        {"user_id": user["id"], "email": user["email"]},
        config["development"].SECRET_KEY,
        algorithm="HS256",
    )

    return {"access_token": token}


@jwt_auth_bp.route("/jwt-protected", methods=["GET"], provide_automatic_options=False)
@doc(description="Protected resource using JWT token", tags=["Authentication"])
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
        email = decoded_token["email"]

        # Perform any additional authentication or authorization checks based on user_id or username
        if user_id == 1234:
            return {"message": f"Authorized user {email} with ID {user_id}"}
        return {"message": f"Protected resource for user {email} with ID {user_id}"}
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401


app.register_blueprint(jwt_auth_bp, url_prefix="/login")
DOCS.register(index, blueprint="jwt_auth_bp")
DOCS.register(login, blueprint="jwt_auth_bp")
DOCS.register(protected, blueprint="jwt_auth_bp")
