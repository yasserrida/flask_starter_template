import json
from app import app


def test_index_route():
    """Test users index route

    Returns:
        void
    """
    response = app.test_client().get("/users")

    assert response.status_code == 200
    assert len(json.loads(response.data.decode("utf-8")))


def test_show_route():
    """Test get user route

    Returns:
        void
    """
    response = app.test_client().get("/users/1")

    assert response.status_code == 200


def test_store_route():
    """Test add user route

    Returns:
        void
    """
    response = app.test_client().post(
        "/users",
        json={
            "id": 1,
            "first_name": "test1",
            "last_name": "test1",
            "email": "test1@nttdata.com",
            "password": "123456",
            "birth_date": "01/01/1998",
        },
    )

    assert response.status_code == 200


def test_update_route():
    """Test update user route

    Returns:
        void
    """
    response = app.test_client().put(
        "/users/1",
        json={
            "id": 1,
            "first_name": "test1",
            "last_name": "test1",
            "email": "test1@nttdata.com",
            "password": "123456",
            "birth_date": "02/02/2000",
        },
    )

    assert response.status_code == 200
