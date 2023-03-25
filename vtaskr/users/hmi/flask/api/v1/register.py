from datetime import timedelta

from email_validator import EmailSyntaxError
from flask import current_app, request

from vtaskr.flask.utils import ResponseAPI
from vtaskr.notifications import NotificationService
from vtaskr.redis import rate_limited
from vtaskr.secutity.validators import PasswordComplexityError
from vtaskr.users.hmi.dto.user import UserDTO, UserMapperDTO
from vtaskr.users.hmi.flask.emails import RegisterEmail
from vtaskr.users.hmi.user_service import UserService

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
                "description": "Unauthorized",
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
    Return the jsonify user created
    """

    payload: dict = request.get_json()
    try:
        with current_app.sql.get_session() as session:
            auth_service = UserService(session, testing=current_app.testing)
            password = payload.pop("password")
            user_dto = UserDTO(**payload)
            user = auth_service.register(user_dto, password)

            with current_app.trans.get_translation_session(
                "users", user.locale
            ) as trans:
                register_email = RegisterEmail(trans, [user.email], user.first_name)
            notification = NotificationService(testing=current_app.testing)
            notification.add_message(register_email)
            notification.notify_all()

            user_dto = UserMapperDTO.model_to_dto(user)
            return ResponseAPI.get_response(UserMapperDTO.dto_to_dict(user_dto), 201)
    except (PasswordComplexityError, EmailSyntaxError) as e:
        return ResponseAPI.get_error_response(str(e), 400)
    except KeyError:
        return ResponseAPI.get_error_response("No password given", 400)
    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)