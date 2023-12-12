import json
import os
from flask import request, jsonify, render_template, Blueprint
from bson import ObjectId
from flask_apispec import doc, use_kwargs, marshal_with
from marshmallow import Schema, fields
from app.models.mongo_singleton import MongoDBSingleton
from app.models.film import FilmSchema
from app.config import database_name, collection_film, mongodb_host, port
from app import app, DOCS


data = json.load(open(f"{os.getcwd()}/app/static/films.json"))
films_list = data

db_connector = MongoDBSingleton(
    mongo_url=mongodb_host + "/" + str(port),
    database_name=database_name,
    collection_name=collection_film,
)

film_blueprint = Blueprint("film_blueprint", __name__)


class StringResponseSchema(Schema):
    """Default Response Schema"""

    success = fields.Bool()
    message = fields.Str()


class DataResponseSchema(Schema):
    """Default Response Schema"""

    data = FilmSchema
    success = fields.Str()


@film_blueprint.route("/save", methods=["GET"], provide_automatic_options=False)
@doc(description="Store Films in DB", tags=["Films"])
@marshal_with(StringResponseSchema())
def store_films():
    """save data to DB"""
    try:
        coll = db_connector.get_collection()
        coll.insert_many(data)
        return {"success": True, "message": "data imported"}, 200
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


@film_blueprint.route("/<title>", methods=["GET"], provide_automatic_options=False)
@doc(description="get film by title", tags=["Films"])
@marshal_with(FilmSchema(many=False))
def add(title):
    """get film by title"""
    try:
        existed_coll = db_connector.get_collection()
        film = existed_coll.find_one({"Title": title})
        if film:
            film["_id"] = str(film["_id"])
            return film, 200
        else:
            return jsonify({"message": "Film not found"}), 404
    except Exception as e:
        return jsonify({"message": "fail"}), 400


@film_blueprint.route("/all", methods=["GET"], provide_automatic_options=False)
@doc(description="get all films", tags=["Films"])
@marshal_with(FilmSchema(many=True))
def display():
    """get all films in DB"""
    try:
        existed_coll = db_connector.get_collection()
        films = list(existed_coll.find({}))
        for film in films:
            film["_id"] = str(film["_id"])
        return films, 200
    except Exception as e:
        return {"message": str(e)}, 500


@film_blueprint.route("", methods=["POST"], provide_automatic_options=False)
@doc(description="create film", tags=["Films"])
@use_kwargs(FilmSchema, location="json")
@marshal_with(StringResponseSchema())
def create_film(**kwargs):
    """create film"""
    print(kwargs)
    data_to_create = request.get_json()
    print(data_to_create)
    try:
        existed_coll = db_connector.get_collection()
        existed_coll.insert_one(kwargs)
        return {"success": True, "message": "Film created successfully"}, 200
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@film_blueprint.route("/<title>", methods=["PUT"], provide_automatic_options=False)
@doc(description="update film by title", tags=["Films"])
@use_kwargs(FilmSchema, location="json")
@marshal_with(StringResponseSchema())
def update_film(title, **kwargs):
    """update film by title"""
    try:
        data = request.get_json()
        existed_coll = db_connector.get_collection()
        film = existed_coll.find_one({"Title": title})
        if film:
            existed_coll.update_one({"_id": ObjectId(film["_id"])}, {"$set": data})
            return {"success": True, "message": "Film is updated successfully"}, 200
        else:
            return {"success": False, "message": "Film is Not Found"}, 404
    except Exception as e:
        return {"success": False, "message": str(e)}, 500


@film_blueprint.route("/<title>", methods=["DELETE"], provide_automatic_options=False)
@doc(description="Delete film by title", tags=["Films"])
@marshal_with(StringResponseSchema())
def delete_film(title, **kwargs):
    """delete film by title"""
    try:
        existed_coll = db_connector.get_collection()
        film = existed_coll.find_one({"Title": title})

        if film:
            del_result = existed_coll.delete_one({"Title": title})
            if del_result.deleted_count == 1:
                return {"success": True, "message": "Film is deleted"}, 200
            else:
                return {"success": False, "message": "Film is Not Found"}, 404
        else:
            return {"success": False, "message": "Film is Not Found"}, 404
    except Exception as e:
        return {"success": False, "message": str(e)}


app.register_blueprint(film_blueprint, url_prefix="/films")
DOCS.register(store_films, blueprint="film_blueprint")
DOCS.register(add, blueprint="film_blueprint")
DOCS.register(display, blueprint="film_blueprint")
DOCS.register(create_film, blueprint="film_blueprint")
DOCS.register(update_film, blueprint="film_blueprint")
DOCS.register(delete_film, blueprint="film_blueprint")
