from flask import Blueprint
from flask_apispec import doc
from app import app, DOCS
from app.models.project import Project


controller_blueprint = Blueprint("controller_blueprint", __name__)


@controller_blueprint.route("/", provide_automatic_options=False)
@doc(description="Get Home page", tags=["Home"])
def home_page():
    """home_page"""
    return "hello from homepage"


@controller_blueprint.route("/about")
def about():
    """about"""
    return "about page is here"


@controller_blueprint.route("/get-name")
def get_name():
    """get_name"""
    project = Project("SE4I project")

    return {"name": project.get_name()}


app.register_blueprint(controller_blueprint, url_prefix="/controller")
DOCS.register(home_page, blueprint="controller_blueprint")
