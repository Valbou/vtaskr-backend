from flask import Blueprint, jsonify, render_template
from vtasks.base.config import AVAILABLE_LANGUAGES

base_bp = Blueprint(
    name="base_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@base_bp.route("/", methods=["GET"])
def hello():
    """Just a logo displayed to curious users"""
    return render_template("home.html")


@base_bp.route("/languages", methods=["GET"])
def languages():
    """Return all available languages"""
    return jsonify(AVAILABLE_LANGUAGES)
