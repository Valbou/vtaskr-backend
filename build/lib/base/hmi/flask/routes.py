from json import loads

from flask import Blueprint, jsonify, render_template
from src.base.config import AVAILABLE_LANGUAGES, VERSION
from src.libs.flask.utils import ResponseAPI
from src.libs.openapi.base import openapi

base_bp = Blueprint(
    name="base_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@base_bp.route("/", methods=["GET"])
def hello():
    """Just a logo displayed to curious users"""
    return render_template("home.html", version=VERSION)


@base_bp.route("/languages", methods=["GET"])
def languages():
    """Return all available languages"""
    return jsonify(AVAILABLE_LANGUAGES)


@base_bp.route("/documentation", methods=["GET"])
def api_doc():
    """Return an OpenApi document"""
    result = render_template("openapi.json.jinja2", openapi=openapi)
    data = loads(result)
    return ResponseAPI.get_response(data, 200)
