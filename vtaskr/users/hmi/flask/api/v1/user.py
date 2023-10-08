from datetime import timedelta

from flask import current_app, g, request

from vtaskr.libs.flask.utils import ResponseAPI
from vtaskr.libs.redis import rate_limited
from vtaskr.libs.secutity.validators import PasswordComplexityError
from vtaskr.users.hmi.dto import UserDTO, UserMapperDTO
from vtaskr.users.hmi.flask.decorators import login_required
from vtaskr.users.services import UserService

from .. import V1, logger, openapi, users_bp

api_item = {
    "get": {
        "description": "Get current user data",
        "summary": "Current user data",
        "operationId": "getUser",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/User"}
                    }
                },
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
    },
}
openapi.register_path(f"{V1}/users/me", api_item)


@users_bp.route(f"{V1}/users/me", methods=["GET"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def me():
    """
    URL to get current user informations - Token required

    Need a valid token
    Return a jsonify user
    """
    if g.user:
        user_dto = UserMapperDTO.model_to_dto(g.user)
        return ResponseAPI.get_response(UserMapperDTO.dto_to_dict(user_dto), 200)

    else:
        return ResponseAPI.get_error_response("Invalid token", 403)


api_item = {
    "put": {
        "description": "Update current user",
        "summary": "Update current user",
        "operationId": "putUser",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/User"}
                    }
                },
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Update current user",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/User",
                    }
                }
            },
            "required": True,
        },
    },
    "patch": {
        "description": "Update current user",
        "summary": "Update current user",
        "operationId": "patchUser",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/User"}
                    }
                },
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Update current user",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": "#/components/schemas/User",
                    }
                }
            },
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/users/me/update", api_item)


@users_bp.route(f"{V1}/users/me/update", methods=["PUT", "PATCH"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def update_me():
    """
    URL to modify user informations - Token required

    Need a valid token
    Return a jsonify user updated
    """
    try:
        if g.user is None:
            return ResponseAPI.get_error_response("Invalid token", 401)

        else:
            user_dto = UserDTO(**request.get_json())
            g.user = UserMapperDTO.dto_to_model(user_dto, g.user)

            with current_app.sql.get_session() as session:
                user_service = UserService(session=session)
                user_service.update(g.user)
                user_dto = UserMapperDTO.model_to_dto(g.user)

            return ResponseAPI.get_response(UserMapperDTO.dto_to_dict(user_dto), 200)

    except PasswordComplexityError as e:
        return ResponseAPI.get_error_response(str(e), 400)
