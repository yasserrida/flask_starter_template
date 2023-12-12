import requests
from flask import Blueprint, request, jsonify, render_template
from flask_apispec import doc, use_kwargs, marshal_with
from bson.json_util import dumps
from app.models.user import DefaultResponseSchema
from app.models.project_user import DataStore, DataSchema
from app.config import api
from app import app, DB, DOCS

API_BASE_URL = api

datas_bp = Blueprint(
    "datas_bp", __name__, template_folder="templates", static_folder="static"
)


@datas_bp.route("", methods=["GET"], provide_automatic_options=False)
@doc(description="Get All Datas", tags=["Datas"])
@marshal_with(DataSchema(many=True))
def store_data():
    """Get All Data"""
    cursor = DB.datas.find({}).limit(20)  # type: ignore
    return jsonify(dumps(cursor))


@app.route("/projects/")
def projects():
    """projects"""
    return "The project page"


@app.errorhandler(404)
def page_not_found(error):
    """page_not_found"""
    return render_template("page_not_found.html"), 404


@datas_bp.route("/<int:data_id>", methods=["GET"], provide_automatic_options=False)
@doc(description="Get User", tags=["Datas"])
@marshal_with(DataSchema(many=False))
def indexofcars(data_id):
    """Get user by id

    Args:
        id (int): user id

    Returns:
        dict: User
    """
    user = DB.datas.find_one({"id": data_id})  # type: ignore
    if user:
        return jsonify(dumps(user))
    return {"message": "Not existe"}, 400


@datas_bp.route(
    "/update/<int:data_id>", methods=["PUT"], provide_automatic_options=False
)
@doc(description="Update Car", tags=["Datas"])
@use_kwargs(DataSchema, location="json")
@marshal_with(DefaultResponseSchema())
def update(data_id, **kwargs):
    """Update Car

    Args:
        data_id (id)

    Returns:
        str
    """
    try:
        if request.json:
            data_model = DataStore(
                data_id,
                request.json["brand"],
                request.json["model"],
                request.json["year"],
                request.json["des"],
            )
            data_model.update_data()
        return {"message": "success"}, 200
    except Exception:
        return {"message": "Not existe"}, 400


@datas_bp.route("/delete/<int:id>", methods=["DELETE"], provide_automatic_options=False)
@doc(description="Delete Car", tags=["Datas"])
def delete_data(id):
    """Delete Car

    Args:
        id (int)
    Returns:
        str
    """
    response = requests.delete(f"{API_BASE_URL}/{id}")
    if response.status_code == 200:
        return {"message": "Car deleted"}
    else:
        return {"error": "Car not found"}, response.status_code


app.register_blueprint(datas_bp, url_prefix="/datas")
DOCS.register(indexofcars, blueprint="datas_bp")
DOCS.register(update, blueprint="datas_bp")
DOCS.register(store_data, blueprint="datas_bp")
DOCS.register(delete_data, blueprint="datas_bp")
