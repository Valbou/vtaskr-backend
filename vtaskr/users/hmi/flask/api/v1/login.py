from datetime import timedelta

from flask import current_app, request

from vtaskr.flask.utils import ResponseAPI
from vtaskr.notifications import NotificationService
from vtaskr.redis import rate_limited
from vtaskr.users.hmi.flask.emails import LoginEmail
from vtaskr.users.hmi.user_service import UserService

from .. import V1, logger, openapi, users_bp

api_item = {
    "post": {
        "description": "Endpoint for user login",
        "summary": "To login an user",
        "operationId": "postLogin",
        "responses": {
            "201": {
                "description": "Return a token to confirm with 2FA",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "object",
                            "properties": {
                                "token": {"type": "string"},
                            },
                        }
                    }
                },
            },
            "400": {
                "description": "Bad request format",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
            "401": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Credentials to login user",
            "content": {
                "application/json": {
                    "schema": {
                        "email": {
                            "type": "string",
                            "required": True,
                            "example": "my@email.com",
                        },
                        "password": {
                            "type": "string",
                            "required": True,
                            "example": "12_aB-34#Cd",
                        },
                    }
                }
            },
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/users/login", api_item)


@users_bp.route(f"{V1}/users/login", methods=["POST"])
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def login():
    """
    URL to login as an authorized user
    Clean all expired tokens, for all users

    Need an email and a password
    Return a valid token
    """
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
