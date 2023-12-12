"""Film Model"""
import json
from marshmallow import Schema, fields


class FilmSchema(Schema):
    """Film Schema"""

    Title = fields.Str(required=False)
    Year = fields.Str(required=False)
    Rated = fields.Str(required=True)


class Film:
    """Film Model"""

    def __init__(self, title, year, rated):
        self.title = title
        self.year = year
        self.rated = rated
        self.films_list = []

    def add_film(self):
        """Add film method"""

        films_list = []
        parsed_films = json.load(open("app/static/users_list.json", encoding="utf-8"))
        if len(parsed_films):
            films_list = parsed_films

        self.films_list.append(
            {"Title": self.title, "Year": self.year, "Rated": self.rated}
        )

        json.dump(
            films_list,
            json.load(open("app/static/users_list.json", encoding="utf-8")),
            indent=4,
            separators=(",", ": "),
        )
