""" Post Model """

from marshmallow import Schema, fields
from app import SQL_DB


class PostSchema(Schema):
    """Post Schema"""

    id = fields.Int(required=True)
    title = fields.Str(required=True, nullable=False)
    content = fields.Str(required=True,)


# pylint: disable=C0103
class Post(SQL_DB.Model):
    """Post Class"""

    id = SQL_DB.Column(SQL_DB.Integer, primary_key=True)
    title = SQL_DB.Column(SQL_DB.String(255), nullable=False)
    content = SQL_DB.Column(SQL_DB.String(255), nullable=False)

    def store(self):
        """Add new post

        Returns:
            void
        """
        SQL_DB.session.add(self)
        SQL_DB.session.commit()

    def update(self, title: str, content: str):
        """Update post

        Args:
            title: str
            content: str

        Returns:
            void
        """
        self.title = title
        self.content = content
        SQL_DB.session.commit()

    def delete(self):
        """Delete post

        Returns:
            void
        """
        SQL_DB.session.delete(self)
        SQL_DB.session.commit()
