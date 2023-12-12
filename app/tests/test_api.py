from app import app
import json


def test_index_route():
    response = app.test_client().get("/controller/")

    assert response.status_code == 200
    # assert response.data.decode("utf-8") == "hello from homepage"


def test_get_name_route():
    response = app.test_client().get("/controller/get-name")
    data = json.loads(response.data)
    name = data["name"]
    assert response.status_code == 200
    assert name == "SE4I project"


def test_get():
    response = app.test_client().get("/api/items/1")
    assert response.status_code == 200


def test_post():
    response = app.test_client().post(
        "/api/items", json={"title": "Test Title", "body": "Test Body", "userId": 1}
    )
    assert response.status_code == 201


def test_put():
    response = app.test_client().put(
        "/api/items/1",
        json={"title": "Updated Title", "body": "Updated Body", "userId": 1},
    )
    assert response.status_code == 200


def test_delete():
    response = app.test_client().delete("/api/items/1")
    assert response.status_code == 200
