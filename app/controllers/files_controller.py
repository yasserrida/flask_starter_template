import os
from flask import Blueprint, request, jsonify
from flask_apispec import doc, marshal_with
from werkzeug.utils import secure_filename
from app import app, DOCS
from app.models.user import DefaultResponseSchema, DefaultFileResponseSchema


files_bp = Blueprint(
    "files_bp", __name__, template_folder="templates", static_folder="static"
)


@files_bp.route("", methods=["POST"], provide_automatic_options=False)
@doc(description="Upload a file", tags=["Files"])
@marshal_with(DefaultResponseSchema())
def upload_file():
    """Upload one or muliple files

    Returns:
        str: message
    """
    try:
        # --------- One file upload
        if request.files["file"]:
            file = request.files["file"]
            file.save(f"{os.getcwd()}/uploads/{secure_filename(str(file.filename))}")  # type: ignore
            return jsonify({"message": "File Uploaded"})
        # -------- Multiple files upload
        elif request.files["files"]:
            files = request.files["files"]
            for file in files:
                file.save(f"{os.getcwd()}/uploads/{secure_filename(str(file.filename))}")  # type: ignore
            return jsonify({"message": "Files Uploaded"})
        else:
            return jsonify({"message": "No file was provided"})
    except Exception:
        return jsonify({"message": "File not Uploaded"})


@files_bp.route("/<filename>", methods=["GET"], provide_automatic_options=False)
@doc(description="Download a file", tags=["Files"])
@marshal_with(DefaultFileResponseSchema())
def download_file(filename):
    """Download file

    Args:
        filename: str

    Returns:
        str: message
    """
    try:
        return jsonify(
            {"message": "File found", "path": f"{os.getcwd()}/uploads/{filename}"}
        )
    except Exception:
        return jsonify({"message": "File not found", "path": ""})


app.register_blueprint(files_bp, url_prefix="/upload")
DOCS.register(upload_file, blueprint="files_bp")
DOCS.register(download_file, blueprint="files_bp")
