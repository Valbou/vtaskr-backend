from datetime import timedelta

from flask import current_app, g, request
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict, list_dto_to_dict, list_models_to_list_dto
from src.libs.hmi.querystring import QueryStringFilter
from src.libs.redis import rate_limited
from src.users.hmi.dto import (
    GROUP_COMPONENT,
    ROLE_COMPONENT,
    GroupDTO,
    GroupMapperDTO,
    RoleMapperDTO,
)
from src.users.hmi.flask.decorators import login_required
from src.users.services import UsersService

from .. import API_ERROR_COMPONENT, V1, logger, openapi, users_bp

api_item = {
    "get": {
        "description": "Get all groups",
        "summary": "Give all groups with optionnal filters",
        "operationId": "getGroups",
        "responses": {
            "200": {
                "description": "",
                "content": {"application/json": {"schema": {"$ref": GROUP_COMPONENT}}},
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
        "description": "Create a new group",
        "summary": "Create a new group and the admin role to the user",
        "operationId": "createGroup",
        "responses": {
            "201": {
                "description": "Created group",
                "content": {"application/json": {"schema": {"$ref": GROUP_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Group to create",
            "content": {"application/json": {"schema": {"$ref": GROUP_COMPONENT}}},
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/groups", api_item)


@users_bp.route(f"{V1}/groups", methods=["GET", "POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=30, period=timedelta(seconds=60))
def groups():
    """
    URL to get current user groups - Token required

    Need a valid token
    Return a list of all groups in which the user have a role
    """

    if request.method == "GET":
        qsf = QueryStringFilter(query_string=request.query_string.decode(), dto=GroupDTO)

        users_service = UsersService(current_app.dependencies)
        groups = users_service.get_all_user_groups(
            user_id=g.user.id, qs_filters=qsf.get_filters()
        )

        groups_dto = list_models_to_list_dto(GroupMapperDTO, groups)
        return ResponseAPI.get_response(list_dto_to_dict(groups_dto), 200)

    if request.method == "POST":
        group_dto = GroupDTO(**request.get_json())

        users_service = UsersService(current_app.dependencies)
        group = users_service.create_new_group(
            user_id=g.user.id, group_name=group_dto.name, is_private=False
        )

        group_dto = GroupMapperDTO.model_to_dto(group)
        return ResponseAPI.get_response(dto_to_dict(group_dto), 201)

    else:
        return ResponseAPI.get_405_response()


api_item = {
    "get": {
        "description": "Get the group with specified id",
        "summary": "Get a group",
        "operationId": "getGroup",
        "parameters": [
            {
                "name": "group_id",
                "in": "path",
                "description": "Id of the group you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "A group",
                "content": {"application/json": {"schema": {"$ref": GROUP_COMPONENT}}},
            },
        },
    },
    "put": {
        "description": "Update group",
        "summary": "Update the group",
        "operationId": "putGroup",
        "parameters": [
            {
                "name": "group_id",
                "in": "path",
                "description": "Id of the group you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated group",
                "content": {"application/json": {"schema": {"$ref": GROUP_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Group to update",
            "content": {"application/json": {"schema": {"$ref": GROUP_COMPONENT}}},
            "required": True,
        },
    },
    "patch": {
        "description": "Update group",
        "summary": "Update the group",
        "operationId": "patchGroup",
        "parameters": [
            {
                "name": "group_id",
                "in": "path",
                "description": "Id of the group you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated group",
                "content": {"application/json": {"schema": {"$ref": GROUP_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Group to update",
            "content": {"application/json": {"schema": {"$ref": GROUP_COMPONENT}}},
            "required": True,
        },
    },
    "delete": {
        "description": "Delete the group with specified id",
        "summary": "Delete a group",
        "operationId": "deleteGroup",
        "parameters": [
            {
                "name": "group_id",
                "in": "path",
                "description": "Id of the group you are looking for",
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
openapi.register_path(f"{V1}/group/{{group_id}}", api_item)


@users_bp.route(
    f"{V1}/group/<string:group_id>", methods=["GET", "PUT", "PATCH", "DELETE"]
)
@login_required(logger)
@rate_limited(logger=logger, hit=30, period=timedelta(seconds=60))
def group(group_id: str):
    users_service = UsersService(current_app.dependencies)
    group = users_service.get_group(user_id=g.user.id, group_id=group_id)

    if group:
        if request.method == "GET":
            group_dto = GroupMapperDTO.model_to_dto(group)
            return ResponseAPI.get_response(dto_to_dict(group_dto), 200)

        if request.method in ["PUT", "PATCH"]:
            group_dto = GroupDTO(**request.get_json())
            group = GroupMapperDTO.dto_to_model(group_dto, group)
            if users_service.update_group(user_id=g.user.id, group=group):
                group_dto = GroupMapperDTO.model_to_dto(group)
                return ResponseAPI.get_response(dto_to_dict(group_dto), 200)
            return ResponseAPI.get_403_response()

        if request.method == "DELETE":
            if users_service.delete_group(user_id=g.user.id, group=group):
                return ResponseAPI.get_response("", 204)
            return ResponseAPI.get_403_response()

        else:
            return ResponseAPI.get_405_response()

    else:
        return ResponseAPI.get_404_response()


api_item = {
    "get": {
        "description": "Get group's members",
        "summary": "Get group's members",
        "operationId": "getGroupMembers",
        "parameters": [
            {
                "name": "group_id",
                "in": "path",
                "description": "Id of the group's members you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "A members list",
                "content": {"application/json": {"schema": {"$ref": ROLE_COMPONENT}}},
            },
        },
    },
}
openapi.register_path(f"{V1}/group/{{group_id}}/members", api_item)


@users_bp.route(f"{V1}/group/<string:group_id>/members", methods=["GET"])
@login_required(logger)
@rate_limited(logger=logger, hit=30, period=timedelta(seconds=60))
def group_members(group_id: str):
    users_service = UsersService(current_app.dependencies)
    roles = users_service.get_group_members(user_id=g.user.id, group_id=group_id)

    if roles:
        roles_dto = list_models_to_list_dto(RoleMapperDTO, roles)
        return ResponseAPI.get_response(list_dto_to_dict(roles_dto), 200)

    else:
        return ResponseAPI.get_403_response()
