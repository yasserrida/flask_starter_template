import requests
import json
from bson import json_util
from bson.objectid import ObjectId
from flask import jsonify, Blueprint
from flask_apispec import doc, use_kwargs, marshal_with
from marshmallow import Schema, fields
from app.models.mongo_singleton import MongoDBSingleton
from app.config import mongodb_host, port, database_name, collection_name, api
from app import app, DOCS


API_BASE_URL = api
REQUEST_TIMEOUT = 10
# Define the Flask Blueprint
posts_bp = Blueprint("posts_bp", __name__)

# Singleton MongoDB connection instance for database 'se4i'
# and collection 'posts' with a custom MongoDB URL
custom_mongo_url = mongodb_host + f":{port}/"
mongo_singleton = MongoDBSingleton(
    mongo_url=custom_mongo_url,
    database_name=database_name,
    collection_name=collection_name,
)


class PostSchema(Schema):
    """Post Schema"""

    _id = fields.Str(data_key="_id")
    title = fields.Str()
    content = fields.Str()


@posts_bp.route("/store", methods=["GET"], provide_automatic_options=False)
@doc(description="Store Data", tags=["Posts"])
def store_data():
    """Fetch data from an external API and store it in the MongoDB collection.

    Returns:
        JSON response: A JSON response indicating the status of the data insertion process.
    """
    response = requests.get(API_BASE_URL, timeout=REQUEST_TIMEOUT)
    if response.status_code == 200:
        api_data = response.json()
        json_data = json.loads(
            json_util.dumps(api_data)
        )  # Convert the ObjectId objects to strings
        inserted_ids = (
            mongo_singleton.get_collection().insert_many(json_data).inserted_ids
        )
        # Convert the inserted_ids to strings as well to avoid serialization issues
        inserted_ids = [str(id) for id in inserted_ids]
        return jsonify(
            {"message": "Data inserted successfully", "inserted_ids": inserted_ids}
        )

    return (
        jsonify({"message": "Failed to fetch data from the API"}),
        response.status_code,
    )


@posts_bp.route("/posts", methods=["POST"], provide_automatic_options=False)
@doc(description="Create Post", tags=["Posts"])
@use_kwargs(PostSchema, location="json")
@marshal_with(PostSchema())
def create_post_mongo(**kwargs):
    """Create a new post in the MongoDB collection.

    Args:
        **kwargs: Keyword arguments containing the data for the new post.

    Returns:
        JSON response: A JSON response containing the created post data.
    """
    data = kwargs
    try:
        collection = mongo_singleton.get_collection()
        # Insert the data into the collection
        post_id = collection.insert_one(data).inserted_id
        data["_id"] = str(post_id)
        return data
    except Exception as exception:
        return {"error": str(exception)}, 500


@posts_bp.route("/posts", methods=["GET"], provide_automatic_options=False)
@doc(description="Get All Posts", tags=["Posts"])
@marshal_with(PostSchema(many=True))
def get_all_posts_mongo():
    """Get all posts from the MongoDB collection.

    Returns:
        JSON response: A JSON response containing the list of all posts.
    """
    try:
        collection = mongo_singleton.get_collection()
        posts = list(collection.find({}))
        for post in posts:
            post["_id"] = str(post["_id"])
        return posts
    except Exception as exception:
        return {"error": str(exception)}, 500


@posts_bp.route("/posts/<post_id>", methods=["GET"], provide_automatic_options=False)
@doc(description="Get Post", tags=["Posts"])
@marshal_with(PostSchema())
def get_post_mongo(post_id):
    """Get a specific post from the MongoDB collection.

    Args:
        post_id (str): The ID of the post to retrieve.

    Returns:
        JSON response: A JSON response containing the retrieved post data or an error message if not found.
    """
    try:
        collection = mongo_singleton.get_collection()
        post = collection.find_one({"_id": ObjectId(post_id)})
        if post:
            post["_id"] = str(post["_id"])
            return post
        return {"message": "Post not found"}, 404
    except Exception as exception:
        return {"error": str(exception)}, 500


@posts_bp.route("/posts/<post_id>", methods=["PUT"], provide_automatic_options=False)
@doc(description="Update Post", tags=["Posts"])
@use_kwargs(PostSchema, location="json")
@marshal_with(PostSchema())
def update_post_mongo(post_id, **kwargs):
    """Update a specific post in the MongoDB collection.

    Args:
        post_id (str): The ID of the post to update.
        **kwargs: Keyword arguments containing the updated data for the post.

    Returns:
        JSON response: A JSON response containing
        the updated post data or an error message if not found.
    """
    data = kwargs
    try:
        collection = mongo_singleton.get_collection()
        # Update the post in the collection
        result = collection.update_one({"_id": ObjectId(post_id)}, {"$set": data})
        if result.modified_count == 1:
            data["_id"] = str(post_id)
            return data
        return {"message": "Post not found"}, 404
    except Exception as exception:
        return {"error": str(exception)}, 500


@posts_bp.route("/posts/<post_id>", methods=["DELETE"], provide_automatic_options=False)
@doc(description="Delete Post", tags=["Posts"])
def delete_post_mongo(post_id):
    """Delete a specific post from the MongoDB collection.

    Args:
        post_id (str): The ID of the post to delete.

    Returns:
        JSON response: A JSON response indicating the status of the deletion process.
    """
    try:
        collection = mongo_singleton.get_collection()
        # Delete the post from the collection
        result = collection.delete_one({"_id": ObjectId(post_id)})
        if result.deleted_count == 1:
            return {"message": "Post deleted successfully"}
        return {"message": "Post not found"}, 404
    except Exception as exception:
        return {"error": str(exception)}, 500


# Register the Blueprint with the Flask application
app.register_blueprint(posts_bp, url_prefix="/api")
# Register the API endpoints with Flask-apispec
DOCS.register(store_data, blueprint="posts_bp")
DOCS.register(create_post_mongo, blueprint="posts_bp")
DOCS.register(get_all_posts_mongo, blueprint="posts_bp")
DOCS.register(get_post_mongo, blueprint="posts_bp")
DOCS.register(update_post_mongo, blueprint="posts_bp")
DOCS.register(delete_post_mongo, blueprint="posts_bp")
