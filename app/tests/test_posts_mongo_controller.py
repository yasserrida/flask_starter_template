from app import app


def test_store_data():
    """Test the '/api/store' endpoint."""
    response = app.test_client().get("/api/store")
    assert response.status_code == 200
    data = response.get_json()
    assert "message" in data
    assert "inserted_ids" in data


def test_create_post_mongo():
    """Test the '/api/posts' endpoint for creating a post."""
    post_data = {
        "title": "Test Post",
        "content": "This is a test post.",
    }
    response = app.test_client().post("/api/posts", json=post_data)
    assert response.status_code == 200
    data = response.get_json()
    assert "_id" in data
    assert data["title"] == post_data["title"]
    assert data["content"] == post_data["content"]


def test_get_all_posts_mongo():
    """Test the '/api/posts' endpoint for getting all posts."""
    response = app.test_client().get("/api/posts")
    assert response.status_code == 200


def test_get_post_mongo():
    """Test the '/api/posts/<post_id>' endpoint for getting a specific post."""
    # Assuming you have some post ID, replace 'POST_ID_HERE' with a valid post ID.
    post_id = "64d0b7f48e8aa379aa707a34"
    response = app.test_client().get(f"/api/posts/{post_id}")
    assert response.status_code in [200, 404]
    data = response.get_json()
    if response.status_code == 200:
        assert "_id" in data
        assert "title" in data
    else:
        assert "message" in data


def test_update_post_mongo():
    """Test the '/api/posts/<post_id>' endpoint for updating a specific post."""
    # Assuming you have some post ID, replace 'POST_ID_HERE' with a valid post ID.
    post_id = "64d0b7f48e8aa379aa707a34"
    updated_data = {
        "title": "Updated Test Post",
        "content": "This post has been updated.",
    }
    response = app.test_client().put(f"/api/posts/{post_id}", json=updated_data)
    assert response.status_code in [200, 404]
    data = response.get_json()
    if response.status_code == 200:
        assert "_id" in data
        assert data["title"] == updated_data["title"]
        assert data["content"] == updated_data["content"]
    else:
        assert "message" in data


def test_delete_post_mongo():
    """Test the '/api/posts/<post_id>' endpoint for deleting a specific post."""
    # Assuming you have some post ID, replace 'POST_ID_HERE' with a valid post ID.
    post_id = "64c2638dd9da151e1db56627"
    response = app.test_client().delete(f"/api/posts/{post_id}")
    assert response.status_code in [200, 404]
    data = response.get_json()
    if response.status_code == 200:
        assert "message" in data
        assert data["message"] == "Post deleted successfully"
    else:
        assert "message" in data
