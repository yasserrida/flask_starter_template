""" Auth Model """

from marshmallow import Schema, fields


class LoginSchema(Schema):
    """LoginnSchema"""

    email = fields.String(required=True)
    password = fields.String(required=True)


class TokenResponseSchema(Schema):
    """TokenResponseSchema"""

    access_token = fields.String()


class ProtectedResponseSchema(Schema):
    """ProtectedResponseSchema"""

    message = fields.String()
