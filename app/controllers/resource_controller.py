from flask_restx import Resource

# from flask_apispec import doc, use_kwargs, marshal_with
# from flask_apispec.views import MethodResource
from app import API, SQL_DB
from app.models.user import User, UserSchema, DefaultResponseSchema

# from app import DOCS


@API.route("/crud/<int:user_id>")
@API.param("user_id", "int")
class UserCrud(Resource):
    """Crud operations for user"""

    # @doc(description="Get user", tags=["Users Crud"])
    # @marshal_with(UserSchema)
    def get(self, user_id):
        """Get user"""
        return SQL_DB.get_or_404(User, user_id)

    # @doc(description="Update user", tags=["Users Crud"])
    # @marshal_with(DefaultResponseSchema)

    def put(self, user_id):
        """Update user"""
        try:
            payload = API.payload
            user = SQL_DB.get_or_404(User, user_id)

            return {"message": "success"}
        except Exception:
            return {"message": "Failed"}

    # @doc(description="Delete user", tags=["Users Crud"])
    # @marshal_with(DefaultResponseSchema)
    def delete(self, user_id):
        """Delete user"""
        try:
            user = SQL_DB.get_or_404(User, user_id)
            SQL_DB.session.delete(user)
            SQL_DB.session.commit()
            return {"message": "success"}
        except Exception:
            return {"message": "Failed"}

    # @doc(description="Insert user", tags=["Users Crud"])
    # @marshal_with(DefaultResponseSchema)
    # @use_kwargs(UserSchema, location="json")
    # def post(self, payload, **kwargs):
    #     """Insert user"""
    #     try:
    #         user = User(
    #             payload["id"],
    #             payload["first_name"],
    #             payload["last_name"],
    #             payload["email"],
    #             payload["password"],
    #             payload["birth_date"],
    #         )
    #         SQL_DB.session.add(user)
    #         SQL_DB.session.commit()
    #         return {"message": "success"}
    #     except Exception:
    #         return {"message": "Failed"}


# DOCS.register(UserCrud, endpoint="user")
