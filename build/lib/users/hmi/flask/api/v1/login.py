from datetime import timedelta

from flask import current_app, request
from src.libs.flask.utils import ResponseAPI
from src.libs.redis import rate_limited
from src.users.hmi.flask.emails import LoginEmail
from src.users.services import UserService

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
                "description": "Login required",
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
                        "type": "object",
                        "properties": {
                            "email": {
                                "type": "string",
                                "example": "my@email.com",
                            },
                            "password": {
                                "type": "string",
                                "example": "12_aB-34#Cd",
                            },
                        },
                        "required": [
                            "email",
                            "password",
                        ],
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
    except Exception as e:
        logger.warning(f"400 Error: {e}")
        return ResponseAPI.get_400_response()

    try:
        with current_app.sql.get_session() as session:
            auth_service = UserService(session)
            token, user = auth_service.authenticate(email, password)

            if token is not None:
                with current_app.trans.get_translation_session(
                    "users", user.locale
                ) as trans:
                    login_email = LoginEmail(
                        trans, [user.email], user.first_name, token.temp_code
                    )

                current_app.notification.add_message(login_email)
                current_app.notification.notify_all()

                data = {"token": token.sha_token}
                return ResponseAPI.get_response(data, 201)
            else:
                logger.warning("401 Error: Request token with invalid credentials")
                return ResponseAPI.get_401_response("Invalid credentials")
    except Exception as e:
        logger.error(f"500 Error: {e}")
        return ResponseAPI.get_500_response()
