from datetime import timedelta

from flask import current_app, g, request
from src.libs.flask.querystring import QueryStringFilter
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict, list_dto_to_dict, list_models_to_list_dto
from src.libs.redis import rate_limited
from src.users.hmi.dto import RIGHT_COMPONENT, RightDTO, RightMapperDTO
from src.users.hmi.flask.decorators import login_required
from src.users.services import RightService, RoleTypeService

from .. import API_ERROR_COMPONENT, V1, logger, openapi, users_bp

api_item = {
    "get": {
        "description": "Get all rights",
        "summary": "Give all rights with optionnal filters",
        "operationId": "getRights",
        "responses": {
            "200": {
                "description": "",
                "content": {"application/json": {"schema": {"$ref": RIGHT_COMPONENT}}},
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
        "description": "Create a new right",
        "summary": "Create a new right",
        "operationId": "createRight",
        "responses": {
            "201": {
                "description": "Created right",
                "content": {"application/json": {"schema": {"$ref": RIGHT_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Right to create",
            "content": {"application/json": {"schema": {"$ref": RIGHT_COMPONENT}}},
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/rights", api_item)


@users_bp.route(f"{V1}/rights", methods=["GET", "POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=60))
def rights():
    """
    URL to get rights allowed to the user - Token required

    Need a valid token
    Return a list of all rights the user can have or use
    """
    with current_app.sql.get_session() as session:
        right_service = RightService(session)

        if request.method == "GET":
            qsf = QueryStringFilter(
                query_string=request.query_string.decode(), dto=RightDTO
            )

            rights = right_service.get_all_rights(g.user.id, qsf.get_filters())
            rights_dto = list_models_to_list_dto(RightMapperDTO, rights)
            return ResponseAPI.get_response(list_dto_to_dict(rights_dto), 200)

        if request.method == "POST":
            right_dto = RightDTO(**request.get_json())

            roletype_service = RoleTypeService(session)
            roletype = roletype_service.get_roletype(g.user.id, right_dto.roletype_id)

            if roletype:
                right = right_service.create_right(
                    user_id=g.user.id,
                    group_id=roletype.group_id,
                    right=RightMapperDTO.dto_to_model(right_dto),
                )

                right_dto = RightMapperDTO.model_to_dto(right)
                return ResponseAPI.get_response(dto_to_dict(right_dto), 201)

            return ResponseAPI.get_404_response(
                message="Associated role type not found", status=404
            )
        else:
            return ResponseAPI.get_405_response()


api_item = {
    "get": {
        "description": "Get the right with specified id",
        "summary": "Get a right",
        "operationId": "getRight",
        "parameters": [
            {
                "name": "right_id",
                "in": "path",
                "description": "Id of the right you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "A right",
                "content": {"application/json": {"schema": {"$ref": RIGHT_COMPONENT}}},
            },
        },
    },
    "put": {
        "description": "Update right",
        "summary": "Update the right",
        "operationId": "putRight",
        "parameters": [
            {
                "name": "right_id",
                "in": "path",
                "description": "Id of the right you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated right",
                "content": {"application/json": {"schema": {"$ref": RIGHT_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Right to update",
            "content": {"application/json": {"schema": {"$ref": RIGHT_COMPONENT}}},
            "required": True,
        },
    },
    "patch": {
        "description": "Update right",
        "summary": "Update the right",
        "operationId": "patchRight",
        "parameters": [
            {
                "name": "right_id",
                "in": "path",
                "description": "Id of the right you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated right",
                "content": {"application/json": {"schema": {"$ref": RIGHT_COMPONENT}}},
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {"schema": {"$ref": API_ERROR_COMPONENT}}
                },
            },
        },
        "requestBody": {
            "description": "Right to update",
            "content": {"application/json": {"schema": {"$ref": RIGHT_COMPONENT}}},
            "required": True,
        },
    },
    "delete": {
        "description": "Delete the right with specified id",
        "summary": "Delete a right",
        "operationId": "deleteRight",
        "parameters": [
            {
                "name": "right_id",
                "in": "path",
                "description": "Id of the right you are looking for",
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
openapi.register_path(f"{V1}/right/{{right_id}}", api_item)


@users_bp.route(
    f"{V1}/right/<string:right_id>", methods=["GET", "PUT", "PATCH", "DELETE"]
)
@login_required(logger)
@rate_limited(logger=logger, hit=10, period=timedelta(seconds=60))
def right(right_id: str):
    with current_app.sql.get_session() as session:
        right_service = RightService(session)
        right = right_service.get_right(g.user.id, right_id)

        if right:
            roletype_service = RoleTypeService(session)
            roletype = roletype_service.get_roletype(g.user.id, right.roletype_id)

            if roletype:
                if request.method == "GET":
                    right_dto = RightMapperDTO.model_to_dto(right)
                    return ResponseAPI.get_response(dto_to_dict(right_dto), 200)

                if request.method in ["PUT", "PATCH"]:
                    right_dto = RightDTO(**request.get_json())
                    right = RightMapperDTO.dto_to_model(right_dto, right)
                    if right_service.update_right(g.user.id, right, roletype):
                        right_dto = RightMapperDTO.model_to_dto(right)
                        return ResponseAPI.get_response(dto_to_dict(right_dto), 200)
                    return ResponseAPI.get_403_response()

                if request.method == "DELETE":
                    if right_service.delete_right(g.user.id, right, roletype):
                        return ResponseAPI.get_response({}, 204)
                    return ResponseAPI.get_403_response()

                else:
                    return ResponseAPI.get_405_response()

        return ResponseAPI.get_404_response()
