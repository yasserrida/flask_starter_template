""" Post Controller """

from flask import Blueprint, jsonify, request
from flask_apispec import doc, use_kwargs, marshal_with
from app.models.post import Post, PostSchema
from app.models.user import DefaultResponseSchema
from app import app, DOCS


posts_bp = Blueprint(
    "posts_bp", __name__, template_folder="templates", static_folder="static"
)


@posts_bp.route("", methods=["GET"], provide_automatic_options=False)
@doc(description="Get All Posts", tags=["Posts"])
@marshal_with(PostSchema(many=True))
def index():
    """Get all posts

    Returns:
        flask.Response
    """
    posts = Post.query.all()
    post_list = []
    for post in posts:
        post_list.append({"id": post.id, "title": post.title, "content": post.content})
    return jsonify({"posts": post_list})


@posts_bp.route("", methods=["POST"], provide_automatic_options=False)
@doc(description="Create Post", tags=["Posts"])
@use_kwargs(PostSchema, location="json")
@marshal_with(DefaultResponseSchema())
def store(**kwargs):
    """Create a new post

    Returns:
        flask.Response
    """
    payload = request.get_json()
    post = Post(title=payload.get("title"), content=payload.get("content"))
    post.store()
    return jsonify({"message": "Post created successfully"})


@posts_bp.route("/<int:post_id>", methods=["GET"], provide_automatic_options=False)
@doc(description="Get Post", tags=["Posts"])
@marshal_with(PostSchema(many=False))
def show(post_id):
    """Get a post by ID

    Args:
        post_id (int): post id

    Returns:
        flask.Response
    """
    post = Post.query.get(post_id)
    if post:
        return jsonify({"id": post.id, "title": post.title, "content": post.content})
    return jsonify({"message": "Post not found"})


@posts_bp.route("/<int:post_id>", methods=["PUT"], provide_automatic_options=False)
@doc(description="Update Post", tags=["Posts"])
@use_kwargs(PostSchema, location="json")
@marshal_with(DefaultResponseSchema())
def update(post_id):
    """Update a post by ID

    Args:
        post_id (int): post id

    Returns:
        flask.Response
    """
    post = Post.query.get(post_id)
    if post:
        payload = request.get_json()
        post.update(payload.get("title"), payload.get("content"))
        return jsonify({"message": "Post updated successfully"})
    return jsonify({"message": "Post not found"})


@posts_bp.route("/<int:post_id>", methods=["DELETE"], provide_automatic_options=False)
@doc(description="Delete Post", tags=["Posts"])
@marshal_with(DefaultResponseSchema())
def delete(post_id):
    """Delete a post by ID

    Args:
        post_id (int): post id

    Returns:
        flask.Response
    """
    post = Post.query.get(post_id)
    if post:
        post.delete()
        return jsonify({"message": "Post deleted successfully"})
    return jsonify({"message": "Post not found"})


app.register_blueprint(posts_bp, url_prefix="/posts")
DOCS.register(index, blueprint="posts_bp")
DOCS.register(store, blueprint="posts_bp")
DOCS.register(show, blueprint="posts_bp")
DOCS.register(update, blueprint="posts_bp")
