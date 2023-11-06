from datetime import timedelta

from flask import current_app, g, request
from src.libs.flask.querystring import QueryStringFilter
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict, list_dto_to_dict, list_models_to_list_dto
from src.libs.redis import rate_limited
from src.users.hmi.dto import ROLE_COMPONENT, RoleDTO, RoleMapperDTO
from src.users.hmi.flask.decorators import login_required
from src.users.services import RoleService

from .. import API_ERROR_COMPONENT, V1, logger, openapi, users_bp

api_item = {
    "get": {
        "description": "Get all roles",
        "summary": "Give all roles with optionnal filters",
        "operationId": "getRoles",
        "responses": {
            "200": {
                "description": "",
                "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            },
            "403": {
                "description": "Unauthorized",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
    },
    "post": {
        "description": "Create a new role",
        "summary": "Create a new role if user id a group's admin",
        "operationId": "createRole",
        "responses": {
            "201": {
                "description": "Created role",
                "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Role to create",
            "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/roles", api_item)


@users_bp.route(f"{V1}/roles", methods=["GET", "POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=60))
def roles():
    """
    URL to get current user roles - Token required

    Need a valid token
    Return a list of all roles in which the user have rights
    """

    if request.method == "GET":
        with current_app.sql.get_session() as session:
            qsf = QueryStringFilter(
                query_string=request.query_string.decode(), dto=RoleDTO
            )

            role_service = RoleService(session)
            roles = role_service.get_all_roles(g.user.id, qsf.get_filters())

            roles_dto = list_models_to_list_dto(RoleMapperDTO, roles)
            return ResponseAPI.get_response(list_dto_to_dict(roles_dto), 200)

    if request.method == "POST":
        role_dto = RoleDTO(**request.get_json())

        with current_app.sql.get_session() as session:
            role_service = RoleService(session)
            role = role_service.create_role(
                g.user.id,
                RoleMapperDTO.dto_to_model(role_dto),
            )

            role_dto = RoleMapperDTO.model_to_dto(role)
            return ResponseAPI.get_response(dto_to_dict(role_dto), 201)

    else:
        return ResponseAPI.get_405_response()


api_item = {
    "get": {
        "description": "Get the role with specified id",
        "summary": "Get a role",
        "operationId": "getRole",
        "parameters": [
            {
                "name": "role_id",
                "in": "path",
                "description": "Id of the role you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "A role",
                "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            },
        },
    },
    "put": {
        "description": "Update role",
        "summary": "Update the role",
        "operationId": "putRole",
        "parameters": [
            {
                "name": "role_id",
                "in": "path",
                "description": "Id of the role you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated role",
                "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Role to update",
            "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            "required": True,
        },
    },
    "patch": {
        "description": "Update role",
        "summary": "Update the role",
        "operationId": "patchRole",
        "parameters": [
            {
                "name": "role_id",
                "in": "path",
                "description": "Id of the role you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated role",
                "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Role to update",
            "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            "required": True,
        },
    },
    "delete": {
        "description": "Delete the role with specified id",
        "summary": "Delete a role",
        "operationId": "deleteRole",
        "parameters": [
            {
                "name": "role_id",
                "in": "path",
                "description": "Id of the role you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "204": {
                "description": "no content",
                "content": {},
            },
        },
    },
}
openapi.register_path(f"{V1}/role/{{role_id}}", api_item)


@users_bp.route(
    f"{V1}/role/<string:role_id>", methods=["GET", "PUT", "PATCH", "DELETE"]
)
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def role(role_id: str):
    with current_app.sql.get_session() as session:
        role_service = RoleService(session)
        role = role_service.get_role(g.user.id, role_id)

        if role:
            if request.method == "GET":
                role_dto = RoleMapperDTO.model_to_dto(role)
                return ResponseAPI.get_response(dto_to_dict(role_dto), 200)

            if request.method in ["PUT", "PATCH"]:
                role_dto = RoleDTO(**request.get_json())
                role = RoleMapperDTO.dto_to_model(role_dto, role)

                if role_service.update_role(g.user.id, role):
                    role_dto = RoleMapperDTO.model_to_dto(role)
                    return ResponseAPI.get_response(dto_to_dict(role_dto), 200)
                return ResponseAPI.get_403_response()

            if request.method == "DELETE":
                if role_service.delete_role(g.user.id, role):
                    return ResponseAPI.get_response({}, 204)
                return ResponseAPI.get_403_response()

            else:
                return ResponseAPI.get_405_response()

        else:
            return ResponseAPI.get_404_response()
