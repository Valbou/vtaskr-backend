from datetime import timedelta

from flask import current_app, g, request
from src.libs.flask.querystring import QueryStringFilter
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict, list_dto_to_dict, list_models_to_list_dto
from src.libs.iam.flask.config import login_required
from src.libs.redis import rate_limited
from src.tasks.hmi.dto import TagDTO, TagMapperDTO, TaskDTO, TaskMapperDTO
from src.tasks.services import TagService, TaskService

from .. import V1, logger, openapi, tasks_bp

api_item = {
    "get": {
        "description": "Get all current tenant's tags",
        "summary": "Get tenant's tags",
        "operationId": "getTenantTags",
        "responses": {
            "200": {
                "description": "Tag list",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Tag"},
                        }
                    }
                },
            },
        },
    },
    "post": {
        "description": "Create tag for the current tenant",
        "summary": "Create a tag",
        "operationId": "postTag",
        "responses": {
            "201": {
                "description": "Created tag",
                "content": {
                    "application/json": {"schema": {"$ref": "#/components/schemas/Tag"}}
                },
            },
            "400": {
                "description": "Bad request",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/APIError"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Tag to create",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Tag"}}
            },
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/tags", api_item)


@tasks_bp.route(f"{V1}/tags", methods=["GET", "POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=1, period=timedelta(seconds=1))
def tags():
    """URL to current tenant tags - Token required"""
    if request.method == "GET":
        qsf = QueryStringFilter(query_string=request.query_string.decode(), dto=TaskDTO)

        tag_service = TagService(current_app.dependencies)
        tags = tag_service.get_tags(g.user.id, qsf.get_filters())
        if tags:
            tags_dto = list_models_to_list_dto(TagMapperDTO, tags)
            return ResponseAPI.get_response(list_dto_to_dict(tags_dto), 200)
        else:
            return ResponseAPI.get_response([], 200)

    elif request.method == "POST":
        try:
            tag_dto = TagDTO(**request.get_json())
            tag = TagMapperDTO.dto_to_model(tag_dto)
        except Exception as e:
            logger.warning(f"400 Error: {e}")
            return ResponseAPI.get_400_response(f"Bad request {e}")

        tag_service = TagService(current_app.dependencies)
        tag_service.save_tag(user_id=g.user.id, tag=tag)
        tag_dto = TagMapperDTO.model_to_dto(tag)
        return ResponseAPI.get_response(dto_to_dict(tag_dto), 201)

    else:
        return ResponseAPI.get_405_response()


api_item = {
    "get": {
        "description": "Get the tag with specified id",
        "summary": "Get a tag",
        "operationId": "getTag",
        "parameters": [
            {
                "name": "tag_id",
                "in": "path",
                "description": "Id of the tag you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Created tag",
                "content": {
                    "application/json": {"schema": {"$ref": "#/components/schemas/Tag"}}
                },
            },
        },
    },
    "put": {
        "description": "Update the tag with specified id",
        "summary": "Update a tag",
        "operationId": "putTag",
        "parameters": [
            {
                "name": "tag_id",
                "in": "path",
                "description": "Id of the tag you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated tag",
                "content": {
                    "application/json": {"schema": {"$ref": "#/components/schemas/Tag"}}
                },
            },
        },
        "requestBody": {
            "description": "Tag to update",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Tag"}}
            },
            "required": True,
        },
    },
    "patch": {
        "description": "Update the tag with specified id",
        "summary": "Update a tag",
        "operationId": "patchTag",
        "parameters": [
            {
                "name": "tag_id",
                "in": "path",
                "description": "Id of the tag you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated tag",
                "content": {
                    "application/json": {"schema": {"$ref": "#/components/schemas/Tag"}}
                },
            },
        },
        "requestBody": {
            "description": "Tag to update",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Tag"}}
            },
            "required": True,
        },
    },
    "delete": {
        "description": "Delete the tag with specified id",
        "summary": "Delete a tag",
        "operationId": "deleteTag",
        "parameters": [
            {
                "name": "tag_id",
                "in": "path",
                "description": "Id of the tag you are looking for",
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
openapi.register_path(f"{V1}/tag/{{tag_id}}", api_item)


@tasks_bp.route(f"{V1}/tag/<string:tag_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=1))
def tag(tag_id: str):
    """URL to current tenant tag - Token required"""

    tag_service = TagService(current_app.dependencies)
    tag = tag_service.get_tag(g.user.id, tag_id)

    if tag:
        if request.method == "GET":
            tag_dto = TagMapperDTO.model_to_dto(tag)
            return ResponseAPI.get_response(dto_to_dict(tag_dto), 200)

        elif request.method in ("PUT", "PATCH"):
            tag_dto = TagDTO(**request.get_json())
            tag = TagMapperDTO.dto_to_model(tag_dto, tag)
            tag_service.update_tag(g.user.id, tag)

            tag_dto = TagMapperDTO.model_to_dto(tag)
            return ResponseAPI.get_response(dto_to_dict(tag_dto), 200)

        elif request.method == "DELETE":
            tag_service.delete_tag(g.user.id, tag)
            return ResponseAPI.get_response("", 204)

        else:
            return ResponseAPI.get_405_response()

    else:
        return ResponseAPI.get_404_response()


api_item = {
    "get": {
        "description": "Get all tasks associated to this tag",
        "summary": "Get tasks with this tag",
        "operationId": "getTagTasks",
        "responses": {
            "200": {
                "description": "Task list",
                "content": {
                    "application/json": {
                        "schema": {
                            "type": "array",
                            "items": {"$ref": "#/components/schemas/Task"},
                        }
                    }
                },
            },
        },
        "parameters": [
            {
                "name": "tag_id",
                "in": "path",
                "description": "Id of the tag you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    }
}
openapi.register_path(f"{V1}/tag/{{tag_id}}/tasks", api_item)


@tasks_bp.route(f"{V1}/tag/<string:tag_id>/tasks", methods=["GET"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=1))
def tag_tasks(tag_id: str):
    """Give all tasks associated to a specific tag"""

    if request.method == "GET":
        qsf = QueryStringFilter(query_string=request.query_string.decode(), dto=TaskDTO)

        tag_service = TagService(current_app.dependencies)
        tag = tag_service.get_tag(g.user.id, tag_id)
        if tag:
            task_service = TaskService(current_app.dependencies)
            tasks_dto = list_models_to_list_dto(
                TaskMapperDTO,
                task_service.get_tag_tasks(
                    g.user.id, tag.id, tag.tenant_id, qsf.get_filters()
                ),
            )

            if tasks_dto:
                return ResponseAPI.get_response(list_dto_to_dict(tasks_dto), 200)
            return ResponseAPI.get_response([], 200)
        else:
            return ResponseAPI.get_404_response("Tag not found")
    else:
        return ResponseAPI.get_405_response()
