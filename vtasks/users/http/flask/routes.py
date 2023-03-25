from logging import Logger

from flask import Blueprint, request, current_app

from vtasks.flask.utils import ResponseAPI, get_token
from vtasks.users.persistence import UserDB

from .authenticate import AuthService


logger = Logger(__name__)


users_bp = Blueprint(
    name="users_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


V1 = "/api/v1"


@users_bp.route(f"{V1}/users/register", methods=["POST"])
def register():
    """
    URL to register a new user

    Need: email, password, first_name, last_name, no_bot
    Return the jsonify user created
    """
    payload: dict = request.get_json()
    try:
        with current_app.sql_service.get_session() as session:
            auth_service = AuthService(session)
            user = auth_service.register(payload)
            data = user.to_external_data()
            return ResponseAPI.get_response(data, 201)
    except Exception:
        return ResponseAPI.get_error_response("Bad request", 400)


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
        with current_app.sql_service.get_session() as session:
            auth_service = AuthService(session)
            token = auth_service.authenticate(email, password)

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
    sha_token = get_token(request)
    payload: dict = request.get_json()

    try:
        email = payload.get("email")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql_service.get_session() as session:
            auth_service = AuthService(session)
            if auth_service.logout(email, sha_token):
                data = {}
                return ResponseAPI.get_response(data, 204)
            else:
                return ResponseAPI.get_error_response("Unauthorized", 403)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)


@users_bp.route(f"{V1}/users/me", methods=["GET"])
def me():
    """
    URL to get current user informations - Token required

    Need a valid token
    Return a jsonify user
    """
    try:
        sha_token = get_token(request)
        if not sha_token:
            return ResponseAPI.get_error_response("Invalid token", 401)

        with current_app.sql_service.get_session() as session:
            auth_service = AuthService(session)
            user = auth_service.user_from_token(sha_token)

        if user:
            data = user.to_external_data()
            return ResponseAPI.get_response(data, 200)
        else:
            return ResponseAPI.get_error_response("Invalid token", 401)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)


@users_bp.route(f"{V1}/users/me/update", methods=["PUT", "PATCH"])
def update_me():
    """
    URL to modify user informations - Token required

    Need a valid token
    Return a jsonify user updated
    """
    try:
        sha_token = get_token(request)
        if not sha_token:
            return ResponseAPI.get_error_response("Invalid token", 401)

        with current_app.sql_service.get_session() as session:
            auth_service = AuthService(session)
            user = auth_service.user_from_token(sha_token)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)

    try:
        if user is None:
            return ResponseAPI.get_error_response("Invalid token", 401)
        else:
            user_db = UserDB()
            with current_app.sql_service.get_session() as session:
                user.from_external_data(request.get_json())
                user_db.update(session, user)
                data = user.to_external_data()
            return ResponseAPI.get_response(data, 200)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)
