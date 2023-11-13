from datetime import timedelta

from email_validator import EmailSyntaxError

from flask import current_app, g, request
from src.libs.flask.utils import ResponseAPI
from src.libs.redis import rate_limited
from src.libs.security.validators import get_valid_email
from src.users.hmi.flask.decorators import login_required
from src.users.hmi.flask.emails import ChangeEmailToNewEmail, ChangeEmailToOldEmail
from src.users.services import EmailAlreadyUsedError, UserService

from .. import V1, logger, openapi, users_bp

api_item = {
    "post": {
        "description": "Allow request to change email",
        "summary": "To change email",
        "operationId": "postRequestChangeEmail",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {},
            },
            "400": {
                "description": "Bad request format",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Change for this new email",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "new_email": {
                                "type": "string",
                                "format": "email",
                                "example": "my_new@email.com",
                            }
                        },
                        "required": ["new_email"],
                    }
                }
            },
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/users/me/change-email", api_item)


@users_bp.route(f"{V1}/users/me/change-email", methods=["POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=300))
def change_email():
    """
    URL to request to change email account

    Need a valid token and a new email
    """
    with current_app.sql.get_session() as session:
        payload: dict = request.get_json()
        data = {}
        try:
            new_email = payload.get("new_email", "")
            new_email = get_valid_email(new_email)
            auth_service = UserService(session)
            req_hash, req_code = auth_service.request_email_change(g.user, new_email)
        except (EmailSyntaxError, EmailAlreadyUsedError) as e:
            return ResponseAPI.get_400_response(str(e))
        except AttributeError as e:
            logger.warning(f"400 Error: {e}")
            return ResponseAPI.get_400_response()

        with current_app.trans.get_translation_session("users", g.user.locale) as trans:
            old_email_message = ChangeEmailToOldEmail(
                trans, [g.user.email], g.user.first_name, req_code
            )
            new_email_message = ChangeEmailToNewEmail(
                trans, [new_email], g.user.first_name, req_hash
            )

        current_app.notification.add_message(old_email_message)
        current_app.notification.add_message(new_email_message)
        current_app.notification.notify_all()

        return ResponseAPI.get_response(data, 200)


api_item = {
    "post": {
        "description": "Register new email for an account",
        "summary": "To set new email",
        "operationId": "postSetNewEmail",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {},
            },
            "400": {
                "description": "Bad request format",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "To set the new email to the correct user",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "new_email": {
                                "type": "string",
                                "format": "email",
                                "example": "my_new@email.com",
                            },
                            "old_email": {
                                "type": "string",
                                "format": "email",
                                "example": "my_old@email.com",
                            },
                            "hash": {
                                "type": "string",
                                "example": "a91776c5fbbde1910bc55e7390417d54805a99b0",
                            },
                            "code": {
                                "type": "string",
                                "example": "1A2b3C",
                            },
                        },
                        "required": [
                            "new_email",
                            "old_email",
                            "hash",
                            "code",
                        ],
                    }
                }
            },
            "required": True,
        },
        "security": [],
    },
}
openapi.register_path(f"{V1}/new-email", api_item)


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
        return ResponseAPI.get_400_response()

    try:
        with current_app.sql.get_session() as session:
            user_service = UserService(session)
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
                return ResponseAPI.get_400_response(str(e))
            return ResponseAPI.get_400_response()
    except Exception as e:
        logger.error(f"500 Error: {e}")
        return ResponseAPI.get_500_response()
