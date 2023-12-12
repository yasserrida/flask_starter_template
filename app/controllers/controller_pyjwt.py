import jwt
from flask import Blueprint, request, jsonify, render_template
from flask_apispec import doc, marshal_with
from app import app, DOCS
from app.models.project_user import LoginSchema
from app.config import user_name1, password1, user_id1
from app.config import config


# just to test, the user and pass should be retrieved from database and the pass should be encrypted.
users = {user_name1: {"user_id": user_id1, "password": password1}}
datas_jwt = Blueprint(
    "datas_jwt", __name__, template_folder="templates", static_folder="static"
)


@datas_jwt.route("/pylogin-form", methods=["GET"], provide_automatic_options=False)
@doc(description="Login Page", tags=["Datas"])
@marshal_with(LoginSchema(many=True))
def index1_jwt():
    """Index function"""
    return render_template("login.html")


@datas_jwt.route("/pyjwt-login", methods=["POST"], provide_automatic_options=False)
@doc(description="authontification Page", tags=["Datas"])
@marshal_with(LoginSchema(many=True))
def login1():
    """login1 function"""
    if request.is_json:
        data = request.get_json()
        username = data.get("username")
        password1 = data.get("password")
    else:
        username = request.form.get("username")
        password1 = request.form.get("password")

    if not username or not password1:
        return jsonify({"message": "Missing username or password"}), 400

    if username not in users or users[username]["password"] != password1:
        return jsonify({"message": "Invalid username or password"}), 401

    payload = {"user_id": users[username]["user_id"], "username": username}
    token = jwt.encode(payload, app.config["SECRET_KEY"], algorithm="HS256")

    return jsonify({"access_token": str(token)})


@app.route("/pyjwt-protected", methods=["GET"])
def protected1():
    """protected1 function"""
    # token = requests.post('http://127.0.0.1:8080/pyjwt-login',data={"username":user_name1,"password":password1}).json()["access_token"]
    token = request.headers.get("Authorization")
    if not token:
        return jsonify({"message": "Missing token"}), 401

    try:
        key = config["development"].SECRET_KEY
        decoded_token = jwt.decode(token, key, ["HS256"])
        user_id_token = decoded_token["user_id"]
        username = decoded_token["username"]

        # Perform any additional authentication or authorization checks based on user_id or username
        if user_id_token == 1234:
            return jsonify(
                {"message": f"Authorized user {username} with ID {user_id_token}"}
            )
        return jsonify(
            {
                "message": f"Protected resource for user {username} with ID {user_id_token}"
            }
        )
    except jwt.ExpiredSignatureError:
        return jsonify({"message": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"message": "Invalid token"}), 401


app.register_blueprint(datas_jwt, url_prefix="/datas")
DOCS.register(index1_jwt, blueprint="datas_jwt")
DOCS.register(login1, blueprint="datas_jwt")
