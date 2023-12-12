# from flask import session, jsonify, Blueprint
# from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
# from app import DB, app


# auth_bp = Blueprint("auth_bp", __name__)


# @auth_bp.route("", methods=["POST"])
# def login(username, password):
#     """Authenticate user

#     Returns:
#         User|None
#     """
#     user = DB.users.find_one({"email": username, "password": password})  # type: ignore
#     if user:
#         session["username"] = f"{user['first_name']} {user['last_name']}"
#         access_token = create_access_token(identity=username)
#         return jsonify({"access_token": access_token}), 200
#     session["username"] = None
#     return jsonify({"message": "email or password is incorrect"}), 400


# @auth_bp.route("/me", methods=["POST"])
# @jwt_required()
# def identity():
#     """Get current user

#     Returns:
#         User|None
#     """
#     return get_jwt_identity()


# app.register_blueprint(auth_bp, url_prefix="/auth")
