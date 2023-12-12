from marshmallow import Schema, fields
from app import DB, SQL_DB


class DataSchema(Schema):
    """Data Schema"""

    id = fields.Int(required=True)
    brand = fields.Str(required=True)
    model = fields.Str(required=True)
    year = fields.Int(required=True)
    des = fields.Str(required=True)


class LoginSchema(Schema):
    """Login Schema"""

    id = fields.Int(required=True)
    user_name = fields.Str(required=True)
    password = fields.Str(required=True)


class Project_user:
    def __init__(self, dec) -> None:
        self.dec = dec

    def get_dec(self):
        """Get dec

        Returns:
            str
        """
        return self.dec

    def home_page(self):
        """return home"""
        return self


class Student(SQL_DB.Model):
    """Student model"""

    id = SQL_DB.Column(SQL_DB.Integer, primary_key=True)
    firstname = SQL_DB.Column(SQL_DB.String(100), nullable=False)
    lastname = SQL_DB.Column(SQL_DB.String(100), nullable=False)
    email = SQL_DB.Column(SQL_DB.String(80), unique=True, nullable=False)
    age = SQL_DB.Column(SQL_DB.Integer)
    bio = SQL_DB.Column(SQL_DB.Text)


class DataStore:
    """DataStore model"""

    def __init__(self, id, brand, model, year, des):
        self.id = id
        self.brand = brand
        self.model = model
        self.year = year
        self.description = des

    def __init1__(self):
        self.datas = []
        self.next_id = 1

    def create_data(self, id, brand, model, year, description):
        """_summary_

        Args:
            id (int)
            brand (str)
            model (str)
            year (str)
            description (str)

        Returns:
            data
        """
        data = DataStore(id, brand, model, year, description)
        self.datas.append(data)
        self.next_id += 1
        return data

    def get_data(self, data_id):
        """Get data

        Returns:
            data|None
        """
        for data in self.datas:
            if data.id == data_id:
                return data
        return None

    def update_data(self):
        """Update user

        Returns:
            void
        """
        DB.datas.update_one(
            {"id": self.id},
            {
                "$set": {
                    "brand": self.brand,
                    "model": self.model,
                    "year": self.year,
                    "des": self.description,
                }
            },
        )

    def delete_data(self, data_id):
        """Delete user

        Returns:
            data|None
        """
        data = self.get_data(data_id)
        if data:
            self.datas.remove(data)
            return data
        return None
