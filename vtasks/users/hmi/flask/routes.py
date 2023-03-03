from logging import Logger
from datetime import timedelta

from flask import Blueprint, request, current_app
from email_validator import EmailSyntaxError

from vtasks.flask.utils import ResponseAPI, get_bearer_token, get_ip
from vtasks.redis.ratelimit import RateLimit, LimitExceededError
from vtasks.users.persistence import UserDB, TokenDB
from vtasks.secutity.validators import PasswordComplexityError, get_valid_email
from vtasks.notifications import NotificationService

from .user_service import UserService, EmailAlreadyUsedError
from .email_content import (
    RegisterEmail,
    LoginEmail,
    ChangePasswordEmail,
    ChangeEmailToOldEmail,
    ChangeEmailToNewEmail,
)


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
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            get_ip(request),
            f"POST:{V1}/users/register",
            5,
            timedelta(seconds=300),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    payload: dict = request.get_json()
    try:
        with current_app.sql.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            user = auth_service.register(payload)

            with current_app.trans.get_translation_session(
                "users", user.locale
            ) as trans:
                register_email = RegisterEmail(trans, [user.email], user.first_name)
            notification = NotificationService(testing=current_app.testing)
            notification.add_message(register_email)
            notification.notify_all()

            data = user.to_external_data()
            return ResponseAPI.get_response(data, 201)
    except (PasswordComplexityError, EmailSyntaxError) as e:
        return ResponseAPI.get_error_response(str(e), 400)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


# https://medium.com/swlh/creating-middlewares-with-python-flask-166bd03f2fd4
@users_bp.route(f"{V1}/users/login", methods=["POST"])
def login():
    """
    URL to login as an authorized user
    Clean all expired tokens, for all users

    Need an email and a password
    Return a valid token
    """
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            get_ip(request),
            f"POST:{V1}/users/login",
            5,
            timedelta(seconds=60),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    payload: dict = request.get_json()

    try:
        email = payload.get("email", "")
        password = payload.get("password", "")
    except Exception:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            token, user = auth_service.authenticate(email, password)

            if token is not None:
                with current_app.trans.get_translation_session(
                    "users", user.locale
                ) as trans:
                    login_email = LoginEmail(
                        trans, [user.email], user.first_name, token.temp_code
                    )
                notification = NotificationService(testing=current_app.testing)
                notification.add_message(login_email)
                notification.notify_all()

                data = {"token": token.sha_token}
                return ResponseAPI.get_response(data, 201)
            else:
                return ResponseAPI.get_error_response("Invalid credentials", 401)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


@users_bp.route(f"{V1}/users/2fa", methods=["POST"])
def confirm_2FA():
    """
    URL to confirm 2FA auth - Token required

    Need a valid temp token and a code
    Return a 200
    """
    sha_token = get_bearer_token(request)
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            sha_token or get_ip(request),
            f"POST:{V1}/users/2fa",
            3,
            timedelta(seconds=60),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    if not sha_token:
        return ResponseAPI.get_error_response("Invalid token", 401)

    payload: dict = request.get_json()

    try:
        code = payload.get("code_2FA")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql.get_session() as session:
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
        return ResponseAPI.get_error_response("Internal error", 500)


@users_bp.route(f"{V1}/users/logout", methods=["DELETE"])
def logout():
    """
    URL to logout a logged in user - Token required

    Need a valid token and the user email
    Return a 204
    """
    sha_token = get_bearer_token(request)
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            sha_token or get_ip(request),
            f"DELETE:{V1}/users/logout",
            6,
            timedelta(seconds=60),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    payload: dict = request.get_json()

    try:
        email = payload.get("email", "")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            if auth_service.logout(email, sha_token):
                data = {}
                return ResponseAPI.get_response(data, 204)
            else:
                return ResponseAPI.get_error_response("Unauthorized", 403)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


@users_bp.route(f"{V1}/users/me", methods=["GET"])
def me():
    """
    URL to get current user informations - Token required

    Need a valid token
    Return a jsonify user
    """
    sha_token = get_bearer_token(request)
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            sha_token or get_ip(request),
            f"GET:{V1}/users/me",
            5,
            timedelta(seconds=60),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    try:
        if not sha_token:
            return ResponseAPI.get_error_response("Invalid token", 401)

        with current_app.sql.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            user = auth_service.user_from_token(sha_token)

        if user:
            data = user.to_external_data()
            return ResponseAPI.get_response(data, 200)
        else:
            return ResponseAPI.get_error_response("Invalid token", 403)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


@users_bp.route(f"{V1}/users/me/update", methods=["PUT", "PATCH"])
def update_me():
    """
    URL to modify user informations - Token required

    Need a valid token
    Return a jsonify user updated
    """
    sha_token = get_bearer_token(request)
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            sha_token or get_ip(request),
            f"PUT:{V1}/users/me/update",
            5,
            timedelta(seconds=60),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    try:
        if not sha_token:
            return ResponseAPI.get_error_response("Invalid token", 401)

        with current_app.sql.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            user = auth_service.user_from_token(sha_token)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)

    try:
        if user is None:
            return ResponseAPI.get_error_response("Invalid token", 401)
        else:
            user_db = UserDB()
            with current_app.sql.get_session() as session:
                user.from_external_data(request.get_json())
                user_db.update(session, user)
                data = user.to_external_data()
            return ResponseAPI.get_response(data, 200)
    except PasswordComplexityError as e:
        return ResponseAPI.get_error_response(str(e), 400)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


@users_bp.route(f"{V1}/forgotten-password", methods=["POST"])
def forgotten_password():
    """
    URL to request to change password

    Need the user email
    """
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            get_ip(request),
            f"POST:{V1}/forgotten-password",
            5,
            timedelta(seconds=300),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    payload: dict = request.get_json()
    data = {}

    try:
        email = payload.get("email", "")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        user_db = UserDB()
        with current_app.sql.get_session() as session:
            user = user_db.find_login(session, email)
            if user:
                user_service = UserService(session, testing=current_app.testing)
                request_hash = user_service.request_password_change(user)
                with current_app.trans.get_translation_session(
                    "users", user.locale
                ) as trans:
                    change_password_email = ChangePasswordEmail(
                        trans, [user.email], user.first_name, request_hash
                    )
                notification = NotificationService(testing=current_app.testing)
                notification.add_message(change_password_email)
                notification.notify_all()
        return ResponseAPI.get_response(data, 200)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_response(data, 200)


@users_bp.route(f"{V1}/new-password", methods=["POST"])
def new_password():
    """
    URL to set a new password

    Need the hash sent by email, the email and the new password
    """
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            get_ip(request),
            f"POST:{V1}/new-password",
            5,
            timedelta(seconds=300),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    payload: dict = request.get_json()

    try:
        email = payload.get("email", "")
        request_hash = payload.get("hash", "")
        new_passwd = payload.get("new_password", "")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql.get_session() as session:
            user_service = UserService(session, testing=current_app.testing)
            try:
                if (
                    email
                    and request_hash
                    and new_passwd
                    and user_service.set_new_password(
                        email=email, hash=request_hash, password=new_passwd
                    )
                ):
                    data = {}
                    return ResponseAPI.get_response(data, 200)
            except PasswordComplexityError as e:
                return ResponseAPI.get_error_response(str(e), 400)
            return ResponseAPI.get_error_response("Bad request", 400)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


@users_bp.route(f"{V1}/users/me/change-email", methods=["POST"])
def change_email():
    """
    URL to request to change email account

    Need a valid token and a new email
    """
    sha_token = get_bearer_token(request)
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            sha_token or get_ip(request),
            f"POST:{V1}/users/me/change-email",
            5,
            timedelta(seconds=300),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    try:
        if not sha_token:
            return ResponseAPI.get_error_response("Invalid token", 401)

        with current_app.sql.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            user = auth_service.user_from_token(sha_token)
            if not user:
                return ResponseAPI.get_error_response("Invalid token", 401)

            payload: dict = request.get_json()
            data = {}

            try:
                new_email = payload.get("new_email", "")
                new_email = get_valid_email(new_email)
                req_hash, req_code = auth_service.request_email_change(user, new_email)
            except (EmailSyntaxError, EmailAlreadyUsedError) as e:
                return ResponseAPI.get_error_response(str(e), 400)
            except AttributeError:
                return ResponseAPI.get_error_response("Bad request", 400)

            with current_app.trans.get_translation_session(
                "users", user.locale
            ) as trans:
                old_email_message = ChangeEmailToOldEmail(
                    trans, [user.email], user.first_name, req_code
                )
                new_email_message = ChangeEmailToNewEmail(
                    trans, [new_email], user.first_name, req_hash
                )
            notification = NotificationService(testing=current_app.testing)
            notification.add_message(old_email_message)
            notification.add_message(new_email_message)
            notification.notify_all()
            return ResponseAPI.get_response(data, 200)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


@users_bp.route(f"{V1}/new-email", methods=["POST"])
def new_email():
    """
    URL to set a new email

    Need a code sent by email to old email, the old email,
    the new email and the hash sent to the new email
    """
    try:
        RateLimit(
            current_app.nosql.get_engine(),
            get_ip(request),
            f"POST:{V1}/new-email",
            5,
            timedelta(seconds=300),
        )()
    except LimitExceededError as e:
        logger.warn(str(e))
        return ResponseAPI.get_error_response("Too many requests", 429)

    payload: dict = request.get_json()

    try:
        old_email = payload.get("old_email", "")
        new_email = payload.get("new_email", "")
        request_hash = payload.get("hash", "")
        code = payload.get("code", "")
    except AttributeError:
        return ResponseAPI.get_error_response("Bad request", 400)

    try:
        with current_app.sql.get_session() as session:
            user_service = UserService(session, testing=current_app.testing)
            try:
                if (
                    old_email
                    and new_email
                    and request_hash
                    and code
                    and user_service.set_new_email(
                        old_email=old_email,
                        new_email=new_email,
                        hash=request_hash,
                        code=code,
                    )
                ):
                    data = {}
                    return ResponseAPI.get_response(data, 200)
            except EmailSyntaxError as e:
                return ResponseAPI.get_error_response(str(e), 400)
            return ResponseAPI.get_error_response("Bad request", 400)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)
