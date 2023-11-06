from datetime import timedelta

from flask import current_app, g, request
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict
from src.libs.redis import rate_limited
from src.users.hmi.dto import USER_COMPONENT, UserDTO, UserMapperDTO
from src.users.hmi.flask.decorators import login_required
from src.users.services import UserService

from .. import API_ERROR_COMPONENT, V1, logger, openapi, users_bp

api_item = {
    "get": {
        "description": "Get current user data",
        "summary": "Current user data",
        "operationId": "getUser",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {"application/json": {"schema": {"$ref": USER_COMPONENT}}},
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
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
    user_dto = UserMapperDTO.model_to_dto(g.user)
    return ResponseAPI.get_response(dto_to_dict(user_dto), 200)


api_item = {
    "put": {
        "description": "Update current user",
        "summary": "Update current user",
        "operationId": "putUser",
        "responses": {
            "200": {
                "description": "no response content",
                "content": {"application/json": {"schema": {"$ref": USER_COMPONENT}}},
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Update current user",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": USER_COMPONENT,
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
                "content": {"application/json": {"schema": {"$ref": USER_COMPONENT}}},
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Update current user",
            "content": {
                "application/json": {
                    "schema": {
                        "$ref": USER_COMPONENT,
                    }
                }
            },
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/users/me", api_item)


@users_bp.route(f"{V1}/users/me", methods=["PUT", "PATCH"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def update_me():
    """
    URL to modify user informations - Token required

    Need a valid token
    Return a jsonify user updated
    """

    user_dto = UserDTO(**request.get_json())
    g.user = UserMapperDTO.dto_to_model(user_dto, g.user)

    with current_app.sql.get_session() as session:
        user_service = UserService(session=session)
        user_service.update(g.user)
        user_dto = UserMapperDTO.model_to_dto(g.user)

    return ResponseAPI.get_response(dto_to_dict(user_dto), 200)


api_item = {
    "delete": {
        "description": "Delete current user",
        "summary": "Delete current user",
        "operationId": "deleteUser",
        "responses": {
            "204": {
                "description": "User deleted",
                "content": {"application/json": {"schema": {"$ref": USER_COMPONENT}}},
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
    },
}


@users_bp.route(f"{V1}/users/me", methods=["DELETE"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def delete_me():
    """
    URL to delete user - Token required

    Need a valid token
    Return a jsonify user deleted
    """

    with current_app.sql.get_session() as session:
        user_service = UserService(session=session)
        if user_service.delete(g.user):
            user_dto = UserMapperDTO.model_to_dto(g.user)

            return ResponseAPI.get_response(dto_to_dict(user_dto), 204)

        return ResponseAPI.get_403_response(
            message=(
                "Check you haven't anymore roles in some groups, "
                "You may need to leave all groups except your private group"
            )
        )
