from flask import jsonify, request
from app import SQL_DB, app


class Film(SQL_DB.Model):
    """Film Class"""

    id = SQL_DB.Column(SQL_DB.Integer, primary_key=True)
    Title = SQL_DB.Column(SQL_DB.String(100))
    Year = SQL_DB.Column(SQL_DB.String(100))
    Rated = SQL_DB.Column(SQL_DB.String(50))


@app.route("/get_all_films", methods=["GET"])
def get_all_films():
    """Route to get all films"""
    films = Film.query.all()
    films_list = []
    for film in films:
        films_list.append(
            {"id": film.id, "Title": film.Title, "Year": film.Year, "Rated": film.Rated}
        )
    return jsonify({"films": films_list})


@app.route("/create_film", methods=["POST"])
def create_afilm():
    """Route to create a new film"""
    data = request.get_json()
    title = data.get("Title")
    Year = data.get("Year")
    Rated = data.get("Rated")
    new_film = Film(Title=title, Year=Year, Rated=Rated)
    SQL_DB.session.add(new_film)
    SQL_DB.session.commit()
    return jsonify({"message": "Film created successfully"})


@app.route("/get_film/<int:film_id>", methods=["GET"])
def get_film(film_id):
    """Route to get a film by ID"""
    film = Film.query.get(film_id)
    if film:
        return jsonify({"id": film.id, "title": film.title, "content": film.content})
    else:
        return jsonify({"message": "Film not found"})


@app.route("/update_film/<int:film_id>", methods=["PUT"])
def update_film(film_id):
    """Route to update a film by ID"""
    film = Film.query.get(film_id)
    if film:
        data = request.get_json()
        film.title = data.get("title")
        film.content = data.get("content")
        SQL_DB.session.commit()
        return jsonify({"message": "Film updated successfully"})
    else:
        return jsonify({"message": "Film not found"})


@app.route("/delete_film/<int:film_id>", methods=["DELETE"])
def delete_film(film_id):
    """Route to delete a film by ID"""
    film = Film.query.get(film_id)
    if film:
        SQL_DB.session.delete(film)
        SQL_DB.session.commit()
        return jsonify({"message": "Film deleted successfully"})
    else:
        return jsonify({"message": "Film not found"})
