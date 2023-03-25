from flask import Blueprint, request, jsonify


users_bp = Blueprint(
    name="users_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@users_bp.route("/login", methods=["POST"])
def login():
    """URL to login as an authorized user"""


@users_bp.route("/login/2fa", methods=["POST"])
def login2fa():
    """URL to send 2FA auth - Token required"""


@users_bp.route("/user", methods=["PUT"])
def user():
    """URL to modify user informations - Token required"""

