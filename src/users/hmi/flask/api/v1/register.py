from datetime import timedelta

from email_validator import EmailSyntaxError

from flask import current_app, request
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict
from src.libs.redis import rate_limited
from src.libs.security.validators import PasswordComplexityError
from src.users.hmi.dto.user import UserDTO, UserMapperDTO
from src.users.hmi.flask.emails import RegisterEmail
from src.users.services import UserService

from .. import V1, logger, openapi, users_bp

api_item = {
    "post": {
        "description": "Register a new user",
        "summary": "Register user",
        "operationId": "postRegister",
        "responses": {
            "201": {
                "description": "no response content",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/User"}
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
            "description": "User to register",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/User",
                        "password": {
                            "type": "string",
                        },
                    }
                }
            },
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/users/register", api_item)


@users_bp.route(f"{V1}/users/register", methods=["POST"])
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=300))
def register():
    """
    URL to register a new user

    Need: email, password, first_name, last_name
    Return the created user
    """

    payload: dict = request.get_json()
    try:
        with current_app.sql.get_session() as session:
            password = payload.pop("password")
            user_dto = UserDTO(**payload)

            auth_service = UserService(session)
            auth_service.clean_unused_accounts()

            user, _group = auth_service.register(user_dto, password)

            with current_app.trans.get_translation_session(
                "users", user.locale
            ) as trans:
                register_email = RegisterEmail(trans, [user.email], user.first_name)

            current_app.notification.add_message(register_email)
            current_app.notification.notify_all()

            user_dto = UserMapperDTO.model_to_dto(user)
            return ResponseAPI.get_response(dto_to_dict(user_dto), 201)

    except (PasswordComplexityError, EmailSyntaxError) as e:
        return ResponseAPI.get_400_response(str(e))

    except KeyError as e:
        logger.warning(f"400 Error: {e}")
        return ResponseAPI.get_400_response("No password given")

    except ValueError as e:
        logger.warning(f"400 Error: {e}")
        return ResponseAPI.get_400_response(f"{e}")

    except Exception as e:
        logger.error(f"500 Error: {e}")
        return ResponseAPI.get_500_response("Internal error")
