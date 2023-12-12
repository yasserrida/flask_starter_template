from flask import jsonify, request
from app import SQL_DB, app


class Post(SQL_DB.Model):
    id = SQL_DB.Column(SQL_DB.Integer, primary_key=True)
    title = SQL_DB.Column(SQL_DB.String(100))
    content = SQL_DB.Column(SQL_DB.String(50))


@app.route("/get_all_posts", methods=["GET"])
def get_all_posts():
    """Route to get all posts"""
    posts = Post.query.all()
    post_list = []
    for post in posts:
        post_list.append({"id": post.id, "title": post.title, "content": post.content})
    return jsonify({"posts": post_list})


@app.route("/create_post", methods=["POST"])
def create_post():
    """Route to create a new post"""
    data = request.get_json()
    title = data.get("title")
    content = data.get("content")
    new_post = Post(title=title, content=content)
    SQL_DB.session.add(new_post)
    SQL_DB.session.commit()
    return jsonify({"message": "Post created successfully"})


@app.route("/get_post/<int:post_id>", methods=["GET"])
def get_post(post_id):
    """Route to get a post by ID"""
    post = Post.query.get(post_id)
    if post:
        return jsonify({"id": post.id, "title": post.title, "content": post.content})
    else:
        return jsonify({"message": "Post not found"})


@app.route("/update_post/<int:post_id>", methods=["PUT"])
def update_post(post_id):
    """Route to update a post by ID"""
    post = Post.query.get(post_id)
    if post:
        data = request.get_json()
        post.title = data.get("title")
        post.content = data.get("content")
        SQL_DB.session.commit()
        return jsonify({"message": "Post updated successfully"})
    else:
        return jsonify({"message": "Post not found"})


@app.route("/delete_post/<int:post_id>", methods=["DELETE"])
def delete_post(post_id):
    """Route to delete a post by ID"""
    post = Post.query.get(post_id)
    if post:
        SQL_DB.session.delete(post)
        SQL_DB.session.commit()
        return jsonify({"message": "Post deleted successfully"})
    else:
        return jsonify({"message": "Post not found"})
