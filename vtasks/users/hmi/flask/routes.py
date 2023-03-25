from logging import Logger

from flask import Blueprint, request, current_app

from vtasks.flask.utils import ResponseAPI, get_bearer_token
from vtasks.users.persistence import UserDB, TokenDB

from vtasks.notifications import NotificationService
from .user_service import UserService
from .email_content import RegisterEmail, LoginEmail


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
            auth_service = UserService(session, testing=current_app.testing)
            user = auth_service.register(payload)

            register_email = RegisterEmail(
                [user.email], user.first_name, user.last_name
            )
            notify = NotificationService(testing=current_app.testing)
            notify.notify_by_email(register_email)

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
            auth_service = UserService(session, testing=current_app.testing)
            token, user = auth_service.authenticate(email, password)

            if token is not None:
                login_email = LoginEmail(
                    [user.email], user.first_name, user.last_name, token.temp_code
                )
                notify = NotificationService(testing=current_app.testing)
                notify.notify_by_email(login_email)

                data = {"token": token.sha_token}
                return ResponseAPI.get_response(data, 201)
            else:
                return ResponseAPI.get_error_response("Invalid credentials", 401)

    except Exception as e:
        print(str(e))
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error: " + str(e), 500)


@users_bp.route(f"{V1}/users/2fa", methods=["POST"])
def confirm_2FA():
    """
    URL to confirm 2FA auth - Token required

    Need a valid temp token and a code
    Return a 200
    """
    sha_token = get_bearer_token(request)
    if not sha_token:
        return ResponseAPI.get_error_response("Invalid token", 401)

    payload: dict = request.get_json()

    try:
        code = payload.get("code_2FA")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql_service.get_session() as session:
            token_db = TokenDB()
            token = token_db.get_token(session, sha_token)
            if code and token.is_temp_valid() and token.validate_token(code):
                session.commit()
                data = {"2FA": "ok"}
                return ResponseAPI.get_response(data, 200)
            else:
                return ResponseAPI.get_error_response("Invalid 2FA code", 401)
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
    sha_token = get_bearer_token(request)
    payload: dict = request.get_json()

    try:
        email = payload.get("email")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql_service.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
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
        sha_token = get_bearer_token(request)
        if not sha_token:
            return ResponseAPI.get_error_response("Invalid token", 401)

        with current_app.sql_service.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            user = auth_service.user_from_token(sha_token)

        if user:
            data = user.to_external_data()
            return ResponseAPI.get_response(data, 200)
        else:
            return ResponseAPI.get_error_response("Invalid token", 403)
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
        sha_token = get_bearer_token(request)
        if not sha_token:
            return ResponseAPI.get_error_response("Invalid token", 401)

        with current_app.sql_service.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
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
