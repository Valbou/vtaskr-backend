from datetime import timedelta

from flask import current_app, g, request
from src.libs.flask.querystring import QueryStringFilter
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict, list_dto_to_dict, list_models_to_list_dto
from src.libs.redis import rate_limited
from src.users.hmi.dto import ROLETYPE_COMPONENT, RoleTypeDTO, RoleTypeMapperDTO
from src.users.hmi.flask.decorators import login_required
from src.users.services import RoleTypeService

from .. import API_ERROR_COMPONENT, V1, logger, openapi, users_bp

api_item = {
    "get": {
        "description": "Get all role types",
        "summary": "Give all role types with optionnal filters",
        "operationId": "getRoleTypes",
        "responses": {
            "200": {
                "description": "",
                "content": {
                    "application/json": {"schema": {"$ref": ROLETYPE_COMPONENT}}
                },
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
        "description": "Create a new role type",
        "summary": "Create a new role type",
        "operationId": "createRoleType",
        "responses": {
            "201": {
                "description": "Created role type",
                "content": {
                    "application/json": {"schema": {"$ref": ROLETYPE_COMPONENT}}
                },
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Role type to create",
            "content": {"application/json": {"schema": {"$ref": ROLETYPE_COMPONENT}}},
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/roletypes", api_item)


@users_bp.route(f"{V1}/roletypes", methods=["GET", "POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=60))
def roletypes():
    """
    URL to get role types allowed to the user - Token required

    Need a valid token
    Return a list of all role types the user can have or use
    """
    with current_app.sql.get_session() as session:
        roletype_service = RoleTypeService(session)

        if request.method == "GET":
            qsf = QueryStringFilter(
                query_string=request.query_string.decode(), dto=RoleTypeDTO
            )

            roletypes = roletype_service.get_all_roletypes(g.user.id, qsf.get_filters())
            roletypes_dto = list_models_to_list_dto(RoleTypeMapperDTO, roletypes)
            return ResponseAPI.get_response(list_dto_to_dict(roletypes_dto), 200)

        if request.method == "POST":
            roletype_dto = RoleTypeDTO(**request.get_json())

            roletype = roletype_service.create_custom_roletype(
                name=roletype_dto.name,
                group_id=roletype_dto.group_id,
            )

            roletype_dto = RoleTypeMapperDTO.model_to_dto(roletype=roletype)
            return ResponseAPI.get_response(dto_to_dict(roletype_dto), 201)

        else:
            return ResponseAPI.get_405_response()


api_item = {
    "get": {
        "description": "Get the role type with specified id",
        "summary": "Get a role type",
        "operationId": "getRoleType",
        "parameters": [
            {
                "name": "roletype_id",
                "in": "path",
                "description": "Id of the role type you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "A role type",
                "content": {
                    "application/json": {"schema": {"$ref": ROLETYPE_COMPONENT}}
                },
            },
        },
    },
    "put": {
        "description": "Update role type",
        "summary": "Update the role type",
        "operationId": "putRoleType",
        "parameters": [
            {
                "name": "roletype_id",
                "in": "path",
                "description": "Id of the role type you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated role type",
                "content": {
                    "application/json": {"schema": {"$ref": ROLETYPE_COMPONENT}}
                },
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Role type to update",
            "content": {"application/json": {"schema": {"$ref": ROLETYPE_COMPONENT}}},
            "required": True,
        },
    },
    "patch": {
        "description": "Update role type",
        "summary": "Update the role type",
        "operationId": "patchRoleType",
        "parameters": [
            {
                "name": "roletype_id",
                "in": "path",
                "description": "Id of the role type you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated role type",
                "content": {
                    "application/json": {"schema": {"$ref": ROLETYPE_COMPONENT}}
                },
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Role type to update",
            "content": {"application/json": {"schema": {"$ref": ROLETYPE_COMPONENT}}},
            "required": True,
        },
    },
    "delete": {
        "description": "Delete the role type with specified id",
        "summary": "Delete a role type",
        "operationId": "deleteRoleType",
        "parameters": [
            {
                "name": "roletype_id",
                "in": "path",
                "description": "Id of the role type you are looking for",
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
openapi.register_path(f"{V1}/roletype/{{roletype_id}}", api_item)


@users_bp.route(
    f"{V1}/roletype/<string:roletype_id>", methods=["GET", "PUT", "PATCH", "DELETE"]
)
@login_required(logger)
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=60))
def roletype(roletype_id: str):
    with current_app.sql.get_session() as session:
        roletype_service = RoleTypeService(session)
        roletype = roletype_service.get_roletype(g.user.id, roletype_id)

        if roletype:
            if request.method == "GET":
                roletype_dto = RoleTypeMapperDTO.model_to_dto(roletype)
                return ResponseAPI.get_response(dto_to_dict(roletype_dto), 200)

            if request.method in ["PUT", "PATCH"]:
                roletype_dto = RoleTypeDTO(**request.get_json())
                if roletype_dto.group_id and roletype_dto.group_id != roletype.group_id:
                    return ResponseAPI.get_403_response(
                        message="You cannot reassign a role type to another group"
                    )

                roletype = RoleTypeMapperDTO.dto_to_model(roletype_dto, roletype)
                if roletype_service.update_roletype(g.user.id, roletype):
                    roletype_dto = RoleTypeMapperDTO.model_to_dto(roletype)
                    return ResponseAPI.get_response(dto_to_dict(roletype_dto), 200)
                return ResponseAPI.get_403_response()

            if request.method == "DELETE":
                if roletype_service.delete_roletype(g.user.id, roletype):
                    return ResponseAPI.get_response("", 204)
                return ResponseAPI.get_403_response()

            else:
                return ResponseAPI.get_405_response()

        return ResponseAPI.get_404_response()
