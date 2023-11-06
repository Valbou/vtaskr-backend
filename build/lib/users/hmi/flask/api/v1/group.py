from datetime import timedelta

from flask import current_app, g, request
from src.libs.flask.querystring import QueryStringFilter
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict, list_dto_to_dict, list_models_to_list_dto
from src.libs.redis import rate_limited
from src.users.hmi.dto import GROUP_COMPONENT, GroupDTO, GroupMapperDTO
from src.users.hmi.flask.decorators import login_required
from src.users.services import GroupService

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
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=60))
def groups():
    """
    URL to get current user groups - Token required

    Need a valid token
    Return a list of all groups in which the user have a role
    """

    if request.method == "GET":
        with current_app.sql.get_session() as session:
            qsf = QueryStringFilter(
                query_string=request.query_string.decode(), dto=GroupDTO
            )

            group_service = GroupService(session)
            groups = group_service.get_all_groups(g.user.id, qsf.get_filters())

            groups_dto = list_models_to_list_dto(GroupMapperDTO, groups)
            return ResponseAPI.get_response(list_dto_to_dict(groups_dto), 200)

    if request.method == "POST":
        group_dto = GroupDTO(**request.get_json())

        with current_app.sql.get_session() as session:
            group_service = GroupService(session)
            group = group_service.create_group(g.user.id, group_dto.name)

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
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=60))
def group(group_id: str):
    with current_app.sql.get_session() as session:
        group_service = GroupService(session)
        group = group_service.get_group(g.user.id, group_id)

        if group:
            if request.method == "GET":
                group_dto = GroupMapperDTO.model_to_dto(group)
                return ResponseAPI.get_response(dto_to_dict(group_dto), 200)

            if request.method in ["PUT", "PATCH"]:
                group_dto = GroupDTO(**request.get_json())
                group = GroupMapperDTO.dto_to_model(group_dto, group)
                if group_service.update_group(g.user.id, group):
                    group_dto = GroupMapperDTO.model_to_dto(group)
                    return ResponseAPI.get_response(dto_to_dict(group_dto), 200)
                return ResponseAPI.get_403_response()

            if request.method == "DELETE":
                if group_service.delete_group(g.user.id, group):
                    return ResponseAPI.get_response("", 204)
                return ResponseAPI.get_403_response()

            else:
                return ResponseAPI.get_405_response()

        else:
            return ResponseAPI.get_404_response()
