from logging import Logger

from flask import Blueprint, request, current_app

from vtasks.flask.utils import ResponseAPI

from .authenticate import AuthService


logger = Logger(__name__)


users_bp = Blueprint(
    name="users_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


V1 = "/api/v1"


# https://medium.com/swlh/creating-middlewares-with-python-flask-166bd03f2fd4
@users_bp.route(f"{V1}/users/login", methods=["POST"])
def login():
    """
    URL to login as an authorized user
    Clean all expired tokens, for all users

    Need an email and a password
    Return a valid token
    """
    payload: dict = request.get_json()

    try:
        email = payload.get("email")
        password = payload.get("password")
    except Exception:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        auth_service = AuthService()
        token = auth_service.authenticate(current_app, email, password)

        if token is not None:
            data = {"token": token}
            return ResponseAPI.get_response(data, 201)
        else:
            return ResponseAPI.get_error_response("Invalid credentials", 401)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)


@users_bp.route(f"{V1}/users/logout", methods=["DELETE"])
def logout():
    """
    URL to logout a logged in user - Token required

    Need a valid token and the user email
    Return a 204
    """
    payload: dict = request.get_json()

    try:
        email = payload.get("email")
        sha_token = payload.get("token")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        auth_service = AuthService()
        if auth_service.logout(current_app, email, sha_token):
            data = {}
            return ResponseAPI.get_response(data, 204)
        else:
            return ResponseAPI.get_error_response("Unauthorized", 403)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)


@users_bp.route(f"{V1}/users/user", methods=["PUT", "PATCH"])
def user():
    """
    URL to modify user informations - Token required

    Need a valid token
    Return a jsonify user updated
    """
