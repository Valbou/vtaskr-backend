from datetime import timedelta

from flask import current_app, request

from vtasks.flask.utils import ResponseAPI
from vtasks.notifications import NotificationService
from vtasks.redis import rate_limited
from vtasks.secutity.validators import PasswordComplexityError
from vtasks.users.hmi.flask.emails import ChangePasswordEmail
from vtasks.users.hmi.user_service import UserService
from vtasks.users.persistence import UserDB

from .. import V1, logger, users_bp


@users_bp.route(f"{V1}/forgotten-password", methods=["POST"])
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=300))
def forgotten_password():
    """
    URL to request to change password

    Need the user email
    """

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
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=300))
def new_password():
    """
    URL to set a new password

    Need the hash sent by email, the email and the new password
    """
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
