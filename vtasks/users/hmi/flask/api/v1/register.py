from datetime import timedelta

from email_validator import EmailSyntaxError
from flask import current_app, request
from vtasks.flask.utils import ResponseAPI
from vtasks.notifications import NotificationService
from vtasks.redis import rate_limited
from vtasks.secutity.validators import PasswordComplexityError
from vtasks.users.hmi.flask.emails import RegisterEmail
from vtasks.users.hmi.user_service import UserService

from .. import V1, logger, users_bp


@users_bp.route(f"{V1}/users/register", methods=["POST"])
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=300))
def register():
    """
    URL to register a new user

    Need: email, password, first_name, last_name, no_bot
    Return the jsonify user created
    """
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
