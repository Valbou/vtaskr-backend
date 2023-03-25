from datetime import timedelta

from email_validator import EmailSyntaxError
from flask import current_app, g, request

from vtaskr.flask.utils import ResponseAPI
from vtaskr.notifications import NotificationService
from vtaskr.redis import rate_limited
from vtaskr.secutity.validators import get_valid_email
from vtaskr.users.hmi.flask.decorators import login_required
from vtaskr.users.hmi.flask.emails import ChangeEmailToNewEmail, ChangeEmailToOldEmail
from vtaskr.users.hmi.user_service import EmailAlreadyUsedError, UserService

from .. import V1, logger, users_bp


@users_bp.route(f"{V1}/users/me/change-email", methods=["POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=300))
def change_email():
    """
    URL to request to change email account

    Need a valid token and a new email
    """
    try:
        with current_app.sql.get_session() as session:
            payload: dict = request.get_json()
            data = {}
            try:
                new_email = payload.get("new_email", "")
                new_email = get_valid_email(new_email)
                auth_service = UserService(session, testing=current_app.testing)
                req_hash, req_code = auth_service.request_email_change(
                    g.user, new_email
                )
            except (EmailSyntaxError, EmailAlreadyUsedError) as e:
                return ResponseAPI.get_error_response(str(e), 400)
            except AttributeError:
                return ResponseAPI.get_error_response("Bad request", 400)

            with current_app.trans.get_translation_session(
                "users", g.user.locale
            ) as trans:
                old_email_message = ChangeEmailToOldEmail(
                    trans, [g.user.email], g.user.first_name, req_code
                )
                new_email_message = ChangeEmailToNewEmail(
                    trans, [new_email], g.user.first_name, req_hash
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
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=300))
def new_email():
    """
    URL to set a new email

    Need a code sent by email to old email, the old email,
    the new email and the hash sent to the new email
    """
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
