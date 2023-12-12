import requests
from flask import Blueprint
from flask_apispec import doc, use_kwargs, marshal_with
from app.config import api
from app.models.item import ItemSchema
from app import app, DOCS


API_BASE_URL = api

# Define the Flask Blueprint
items_bp = Blueprint("items_bp", __name__)


@items_bp.route("/items", methods=["POST"], provide_automatic_options=False)
@doc(description="Create Item", tags=["Items"])
@use_kwargs(ItemSchema, location="json")
@marshal_with(ItemSchema())
def create_item(**kwargs):
    """Create Item"""
    data = kwargs
    response = requests.post(API_BASE_URL, json=data)
    if response.status_code == 201:
        item = response.json()
        return item, 201

    return {"error": "Failed to create item"}, response.status_code


@items_bp.route("/items/<int:id>", methods=["GET"], provide_automatic_options=False)
@doc(description="Get Item", tags=["Items"])
@marshal_with(ItemSchema())
def get_item(id):
    """Get Item"""
    response = requests.get(f"{API_BASE_URL}/{id}")
    if response.status_code == 200:
        item = response.json()
        return item
    else:
        return {"error": "Item not found"}, response.status_code


@items_bp.route("/items/<int:id>", methods=["PUT"], provide_automatic_options=False)
@doc(description="Update Item", tags=["Items"])
@use_kwargs(ItemSchema, location="json")
@marshal_with(ItemSchema())
def update_item(id, **kwargs):
    """Update Item"""
    data = kwargs
    response = requests.put(f"{API_BASE_URL}/{id}", json=data)
    if response.status_code == 200:
        item = response.json()
        return item
    else:
        return {"error": "Item not found"}, response.status_code


@items_bp.route("/items/<int:id>", methods=["DELETE"], provide_automatic_options=False)
@doc(description="Delete Item", tags=["Items"])
def delete_item(id):
    """Delete Item"""
    response = requests.delete(f"{API_BASE_URL}/{id}")
    if response.status_code == 200:
        return {"message": "Item deleted"}
    else:
        return {"error": "Item not found"}, response.status_code


# Register the Blueprint with the Flask application
app.register_blueprint(items_bp, url_prefix="/api")
# Registering the API endpoints with Flask-apispec
DOCS.register(create_item, blueprint="items_bp")
DOCS.register(get_item, blueprint="items_bp")
DOCS.register(update_item, blueprint="items_bp")
DOCS.register(delete_item, blueprint="items_bp")
