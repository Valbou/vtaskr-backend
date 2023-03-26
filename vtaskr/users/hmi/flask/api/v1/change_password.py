from datetime import timedelta

from flask import current_app, request

from vtaskr.flask.utils import ResponseAPI
from vtaskr.notifications import NotificationService
from vtaskr.redis import rate_limited
from vtaskr.secutity.validators import PasswordComplexityError
from vtaskr.users.hmi.flask.emails import ChangePasswordEmail
from vtaskr.users.hmi.user_service import UserService
from vtaskr.users.persistence import UserDB

from .. import V1, logger, openapi, users_bp

api_item = {
    "post": {
        "description": "Allow request to change password",
        "summary": "To change password",
        "operationId": "postRequestChangePassword",
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
            "description": "Email used to login",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "email": {
                                "type": "string",
                                "format": "email",
                                "example": "my@email.com",
                            },
                        },
                        "required": [
                            "email",
                        ],
                    }
                }
            },
            "required": True,
        },
        "security": [],
    },
}
openapi.register_path(f"{V1}/forgotten-password", api_item)


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


api_item = {
    "post": {
        "description": "Allow request to change password",
        "summary": "To set a new password",
        "operationId": "postSetNewPassword",
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
            "description": "To set the new password",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "email": {
                                "type": "string",
                                "format": "email",
                                "example": "my@email.com",
                            },
                            "hash": {
                                "type": "string",
                                "example": "a91776c5fbbde1910bc55e7390417d54805a99b0",
                            },
                            "new_password": {
                                "type": "string",
                                "example": "12_aB-34#Cd",
                            },
                        },
                        "required": [
                            "email",
                            "hash",
                            "new_password",
                        ],
                    }
                }
            },
            "required": True,
        },
        "security": [],
    },
}
openapi.register_path(f"{V1}/new-password", api_item)


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
