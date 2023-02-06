from logging import Logger

from flask import Blueprint, request, current_app

from vtasks.flask.utils import ResponseAPI
from vtasks.users import Token
from vtasks.users.persistence import UserDB, TokenDB


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
    Clean all expired tokens

    Need an email and a password
    Return a temporary token
    """
    payload: dict = request.get_json()

    try:
        email = payload.get("email")
        password = payload.get("password")
    except Exception:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        user_db = UserDB()
        token_db = TokenDB()
        data = {}

        with current_app.sql_service.get_session() as session:
            token_db.clean_expired(session)
            user = user_db.find_login(session, email)
            if not user.check_password(password):
                return ResponseAPI.get_error_response("Invalid credentials", 401)
            else:
                token = Token(user_id=user.id)
                token_db.save(session, token)
                data = {"token": token.sha_token}
        return ResponseAPI.get_response(data, 201)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)


@users_bp.route(f"{V1}/users/login/2fa", methods=["POST"])
def login2fa():
    """
    URL to send 2FA auth - Token required

    Need a temporary token and un numeric code
    Return an expiring token
    (30 minutes after last activity as a classique session)
    """


@users_bp.route(f"{V1}/users/logout", methods=["DELETE"])
def logout():
    """
    URL to logout a logged in user - Token required

    Need a expiring token and the user email
    Return a 204
    """

    payload: dict = request.get_json()

    try:
        email = payload.get("email")
        sha_token = payload.get("token")
    except Exception:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        user_db = UserDB()
        token_db = TokenDB()
        data = {}

        with current_app.sql_service.get_session() as session:
            user = user_db.find_login(session, email)
            token = token_db.get_token(session, sha_token)
            if token.user_id == user.id:
                token_db.delete(session, token)
                return ResponseAPI.get_response(data, 204)
        return ResponseAPI.get_response("Unauthorized", 403)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)


@users_bp.route(f"{V1}/users/user", methods=["PUT", "PATCH"])
def user():
    """
    URL to modify user informations - Token required

    Need an expiring token
    Return a jsonify user updated
    """
