from datetime import timedelta

from flask import current_app, g, request

from vtaskr.libs.flask.querystring import QueryStringFilter
from vtaskr.libs.flask.utils import ResponseAPI
from vtaskr.libs.iam.flask.config import login_required
from vtaskr.libs.redis import rate_limited
from vtaskr.tasks.hmi.dto import TagDTO, TagMapperDTO, TaskDTO, TaskMapperDTO
from vtaskr.tasks.persistence import TagDB
from vtaskr.tasks.services import TagService, TaskService

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
    try:
        if request.method == "GET":
            with current_app.sql.get_session() as session:
                tag_service = TagService(session)
                tags = tag_service.get_tags(g.user.id)
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
    with current_app.sql.get_session() as session:
        tag_service = TagService(session)
        tag = tag_service.get_tag(g.user.id, tag_id)
        if tag:
            if request.method == "GET":
                tag_dto = TagMapperDTO.model_to_dto(tag)
                return ResponseAPI.get_response(TagMapperDTO.dto_to_dict(tag_dto), 200)

            elif request.method in ("PUT", "PATCH"):
                tag_dto = TagDTO(**request.get_json())
                tag = TagMapperDTO.dto_to_model(g.user.id, tag_dto, tag)
                tag_service.update_tag(g.user.id, tag)

                tag_dto = TagMapperDTO.model_to_dto(tag)
                return ResponseAPI.get_response(TagMapperDTO.dto_to_dict(tag_dto), 200)

            elif request.method == "DELETE":
                tag_service.delete_tag(g.user.id, tag)
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
        with current_app.sql.get_session() as session:
            qsf = QueryStringFilter(
                query_string=request.query_string.decode(), dto=TaskDTO
            )

            tag_service = TagService(session)
            tag = tag_service.get_tag(g.user.id, tag_id)
            if tag:
                task_service = TaskService(session)
                tasks_dto = TaskMapperDTO.list_models_to_list_dto(
                    task_service.get_tag_tasks(
                        g.user.id, tag.id, tag.tenant_id, qsf.get_filters()
                    )
                )

                if tasks_dto:
                    return ResponseAPI.get_response(
                        TagMapperDTO.list_dto_to_dict(tasks_dto), 200
                    )
                return ResponseAPI.get_response([], 200)
            else:
                return ResponseAPI.get_error_response("Tag not found", 404)
    else:
        return ResponseAPI.get_error_response({}, 405)
