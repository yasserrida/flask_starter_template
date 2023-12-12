"""User Model"""

from datetime import date, datetime
from marshmallow import Schema, fields
from app import DB, SQL_DB


class DefaultFileResponseSchema(Schema):
    """Default File Response Schema"""

    message = fields.Str()
    path = fields.Str()


class DefaultResponseSchema(Schema):
    """Default Response Schema"""

    message = fields.Str()


class UserSchema(Schema):
    """User Schema"""

    id = fields.Int(required=True)
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    password = fields.Str(required=True)
    birth_date = fields.Str(required=True)


# pylint: disable=C0103
class User(SQL_DB.Model):
    """User Class"""

    id = SQL_DB.Column(SQL_DB.Integer, primary_key=True)
    first_name = SQL_DB.Column(SQL_DB.String(255), nullable=False)
    last_name = SQL_DB.Column(SQL_DB.String(255), nullable=False)
    email = SQL_DB.Column(SQL_DB.String(255), unique=True, nullable=False)
    password = SQL_DB.Column(SQL_DB.String(255), nullable=False)
    birth_date = SQL_DB.Column(SQL_DB.String(255), nullable=False)

    def __init__(self, id, first_name, last_name, email, password, birth_date) -> None:
        self.id = id
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.birth_date = birth_date

    def get_full_name(self):
        """Get user full name

        Returns:
            str: full name
        """
        return f"{self.first_name} {self.last_name.upper()}"

    def get_age(self):
        """Get user age

        Returns:
            int: age
        """
        today = date.today()
        birth_date = datetime.strptime(self.birth_date.replace("/", "-"), "%d-%m-%Y")
        return (
            today.year
            - birth_date.year
            - ((today.month, today.day) < (birth_date.month, birth_date.day))
        )

    def store(self):
        """Add new user

        Returns:
            void
        """
        DB.users.insert_one(
            {
                "id": self.id,
                "first_name": self.first_name,
                "last_name": self.last_name,
                "email": self.email,
                "password": self.password,
                "birth_date": self.birth_date,
            }
        )

    def update(self):
        """Update user

        Returns:
            void
        """
        DB.users.update_one(
            {"id": self.id},
            {
                "$set": {
                    "first_name": self.first_name,
                    "last_name": self.last_name,
                    "email": self.email,
                    "password": self.password,
                    "birth_date": self.birth_date,
                }
            },
        )
