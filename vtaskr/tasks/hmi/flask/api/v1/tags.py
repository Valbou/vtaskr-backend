from datetime import timedelta

from flask import current_app, g, request

from vtaskr.flask.utils import ResponseAPI
from vtaskr.redis import rate_limited
from vtaskr.tasks.hmi.dto import TagDTO, TagMapperDTO, TaskMapperDTO
from vtaskr.tasks.hmi.tags_service import TagService
from vtaskr.tasks.hmi.tasks_service import TaskService
from vtaskr.tasks.persistence import TagDB
from vtaskr.users.hmi.flask.decorators import login_required

from .. import V1, logger, openapi, tasks_bp

api_item = {
    "get": {
        "description": "Get all current user's tags",
        "summary": "Get user's tags",
        "operationId": "getUserTags",
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
        "description": "Create tag for the current user",
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
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Tag"}
                }
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
    """URL to current user tags - Token required"""
    try:
        if request.method == "GET":
            with current_app.sql.get_session() as session:
                tag_service = TagService(session, current_app.testing)
                tags = tag_service.get_user_tags(g.user.id)
                if tags:
                    tags_dto = TagMapperDTO.list_models_to_list_dto(tags)
                    return ResponseAPI.get_response(
                        TagMapperDTO.list_dto_to_dict(tags_dto), 200
                    )
                else:
                    return ResponseAPI.get_response([], 200)

        elif request.method == "POST":
            try:
                tag_dto = TagDTO(**request.get_json())
                tag = TagMapperDTO.dto_to_model(g.user.id, tag_dto)

                with current_app.sql.get_session() as session:
                    tag_db = TagDB()
                    tag_db.save(session, tag)
                    tag_dto = TagMapperDTO.model_to_dto(tag)
                    return ResponseAPI.get_response(
                        TagMapperDTO.dto_to_dict(tag_dto), 201
                    )
            except Exception:
                return ResponseAPI.get_error_response("Bad request", 400)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


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
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Tag"}
                }
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
                "application/json": {
                    "schema": {"$ref": "#/components/schemas/Tag"}
                }
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
    """URL to current user tag - Token required"""
    with current_app.sql.get_session() as session:
        tag_service = TagService(session, current_app.testing)
        tag = tag_service.get_user_tag(g.user.id, tag_id)
        if tag:
            if request.method == "GET":
                tag_dto = TagMapperDTO.model_to_dto(tag)
                return ResponseAPI.get_response(TagMapperDTO.dto_to_dict(tag_dto), 200)

            elif request.method in ("PUT", "PATCH"):
                tag_dto = TagDTO(**request.get_json())
                tag = TagMapperDTO.dto_to_model(g.user.id, tag_dto, tag)
                tag_service.update_user_tag(g.user.id, tag)

                tag_dto = TagMapperDTO.model_to_dto(tag)
                return ResponseAPI.get_response(TagMapperDTO.dto_to_dict(tag_dto), 200)

            elif request.method == "DELETE":
                tag_service.delete_user_tag(g.user.id, tag)
                return ResponseAPI.get_response({}, 204)

        else:
            return ResponseAPI.get_error_response({}, 404)


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
    }
}
openapi.register_path(f"{V1}/tag/{{tag_id}}/tasks", api_item)


@tasks_bp.route(f"{V1}/tag/<string:tag_id>/tasks", methods=["GET"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=1))
def tag_tasks(tag_id: str):
    """Give all tasks associated to a specific tag"""
    if request.method == "GET":
        with current_app.sql.get_session() as session:
            tag_service = TagService(session, current_app.testing)
            tag = tag_service.get_user_tag(g.user.id, tag_id)
            if tag:
                task_service = TaskService(session, current_app.testing)
                tasks_dto = TaskMapperDTO.list_models_to_list_dto(
                    task_service.get_user_tag_tasks(g.user.id, tag.id)
                )
                return ResponseAPI.get_response(
                    TagMapperDTO.list_dto_to_dict(tasks_dto), 200
                )
            else:
                return ResponseAPI.get_error_response("Tag not found", 404)
    else:
        return ResponseAPI.get_error_response({}, 405)
