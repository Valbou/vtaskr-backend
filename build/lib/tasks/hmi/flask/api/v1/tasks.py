from datetime import timedelta

from flask import current_app, g, request

from src.libs.flask.querystring import QueryStringFilter
from src.libs.flask.utils import ResponseAPI
from src.libs.hmi import dto_to_dict, list_dto_to_dict, list_models_to_list_dto
from src.libs.iam.flask.config import login_required
from src.libs.redis import rate_limited
from src.tasks.hmi.dto import TagMapperDTO, TaskDTO, TaskMapperDTO
from src.tasks.services import TagService, TaskService

from .. import V1, logger, openapi, tasks_bp

api_item = {
    "get": {
        "description": "Get all current tenant's tasks",
        "summary": "Get tenant's tasks",
        "operationId": "getTenantTasks",
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
    },
    "post": {
        "description": "Create task for the current tenant",
        "summary": "Create a task",
        "operationId": "postTask",
        "responses": {
            "201": {
                "description": "Created task",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Task"}
                    }
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
            "description": "Task to create",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Task"}}
            },
            "required": True,
        },
    },
}
openapi.register_path(f"{V1}/tasks", api_item)


@tasks_bp.route(f"{V1}/tasks", methods=["GET", "POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=1, period=timedelta(seconds=1))
def tasks():
    """URL to current tenant tasks - Token required"""
    if request.method == "GET":
        with current_app.sql.get_session() as session:
            qsf = QueryStringFilter(
                query_string=request.query_string.decode(), dto=TaskDTO
            )

            task_service = TaskService(session)
            tasks = task_service.get_tasks(g.user.id, qsf.get_filters())
            if tasks:
                tasks_dto = list_models_to_list_dto(TaskMapperDTO, tasks)
                return ResponseAPI.get_response(list_dto_to_dict(tasks_dto), 200)
            else:
                return ResponseAPI.get_response([], 200)

    elif request.method == "POST":
        try:
            task_dto = TaskDTO(**request.get_json())
            task = TaskMapperDTO.dto_to_model(task_dto)

            with current_app.sql.get_session() as session:
                task_service = TaskService(session)
                task_service.save_task(user_id=g.user.id, task=task)
                task_dto = TaskMapperDTO.model_to_dto(task)
                return ResponseAPI.get_response(dto_to_dict(task_dto), 201)
        except Exception:
            return ResponseAPI.get_400_response()

    else:
        return ResponseAPI.get_405_response()


api_item = {
    "get": {
        "description": "Get the task with specified id",
        "summary": "Get a task",
        "operationId": "getTask",
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "description": "Id of the task you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Created task",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Task"}
                    }
                },
            },
        },
    },
    "put": {
        "description": "Update the task with specified id",
        "summary": "Update a task",
        "operationId": "putTask",
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "description": "Id of the task you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated task",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Task"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Task to update",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Task"}}
            },
            "required": True,
        },
    },
    "patch": {
        "description": "Update the task with specified id",
        "summary": "Update a task",
        "operationId": "patchTask",
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "description": "Id of the task you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
        "responses": {
            "200": {
                "description": "Updated task",
                "content": {
                    "application/json": {
                        "schema": {"$ref": "#/components/schemas/Task"}
                    }
                },
            },
        },
        "requestBody": {
            "description": "Task to update",
            "content": {
                "application/json": {"schema": {"$ref": "#/components/schemas/Task"}}
            },
            "required": True,
        },
    },
    "delete": {
        "description": "Delete the task with specified id",
        "summary": "Delete a task",
        "operationId": "deleteTask",
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "description": "Id of the task you are looking for",
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
openapi.register_path(f"{V1}/task/{{task_id}}", api_item)


@tasks_bp.route(
    f"{V1}/task/<string:task_id>", methods=["GET", "PUT", "PATCH", "DELETE"]
)
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=1))
def task(task_id: str):
    """URL to current tenant task - Token required"""
    with current_app.sql.get_session() as session:
        task_service = TaskService(session)
        task = task_service.get_task(g.user.id, task_id)
        if task:
            if request.method == "GET":
                task_dto = TaskMapperDTO.model_to_dto(task)
                return ResponseAPI.get_response(dto_to_dict(task_dto), 200)

            elif request.method in ("PUT", "PATCH"):
                task_dto = TaskDTO(**request.get_json())
                task = TaskMapperDTO.dto_to_model(task_dto, task)
                task_service.update_task(g.user.id, task)

                task_dto = TaskMapperDTO.model_to_dto(task)
                return ResponseAPI.get_response(dto_to_dict(task_dto), 200)

            elif request.method == "DELETE":
                task_service.delete_task(g.user.id, task)
                return ResponseAPI.get_response("", 204)

            else:
                return ResponseAPI.get_405_response()

        else:
            return ResponseAPI.get_404_response()


api_item = {
    "get": {
        "description": "Get all tags associated to this task",
        "summary": "Get tags with this task",
        "operationId": "getTaskTags",
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
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "description": "Id of the task you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    }
}
openapi.register_path(f"{V1}/task/{{task_id}}/tags", api_item)


@tasks_bp.route(f"{V1}/task/<string:task_id>/tags", methods=["GET"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=1))
def task_tags(task_id: str):
    """Get all associated tags to a specific task"""

    if request.method == "GET":
        with current_app.sql.get_session() as session:
            task_service = TaskService(session)
            task = task_service.get_task(g.user.id, task_id)
            if task:
                tag_service = TagService(session)
                tags_dto = list_models_to_list_dto(
                    TagMapperDTO,
                    tag_service.get_task_tags(g.user.id, task.id, task.tenant_id),
                )

                if tags_dto:
                    return ResponseAPI.get_response(list_dto_to_dict(tags_dto), 200)
                return ResponseAPI.get_response([], 200)
            else:
                return ResponseAPI.get_404_response("Task not found")
    else:
        return ResponseAPI.get_405_response()


api_item = {
    "put": {
        "description": "Set tags associated to this task",
        "summary": "Set tags to this task",
        "operationId": "setTaskTags",
        "responses": {
            "201": {
                "description": "Tags associated",
                "content": {},
            },
        },
        "requestBody": {
            "description": "Tags id list",
            "content": {
                "application/json": {
                    "schema": {
                        "type": "object",
                        "properties": {
                            "tags": {
                                "type": "array",
                                "items": {
                                    "type": "string",
                                },
                            }
                        },
                    }
                }
            },
            "required": True,
        },
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "description": "Id of the task you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
}
openapi.register_path(f"{V1}/task/{{task_id}}/tags/set", api_item)


@tasks_bp.route(f"{V1}/task/<string:task_id>/tags/set", methods=["PUT"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=1))
def task_tags_set(task_id: str):
    """Set all associated tags ids to a specific task"""

    data = request.get_json()
    tag_ids = data.get("tags")
    if not isinstance(tag_ids, list):
        logger.warning("400 Error: Invalid parameters - not a list")
        return ResponseAPI.get_400_response()

    for tag_id in tag_ids:
        if not isinstance(tag_id, str):
            logger.warning("400 Error: Invalid parameters - not a list of str")
            return ResponseAPI.get_400_response()

    if request.method == "PUT":
        with current_app.sql.get_session() as session:
            task_service = TaskService(session)
            task = task_service.get_task(g.user.id, task_id)
            try:
                task_service.set_task_tags(g.user.id, task, tag_ids)
            except Exception as e:
                logger.warning(f"400 Error: {e}")
                return ResponseAPI.get_400_response()
            return ResponseAPI.get_response("Created", 201)

    else:
        return ResponseAPI.get_405_response()


api_item = {
    "delete": {
        "description": "Clean associated tags to this task",
        "summary": "Clean task's tags",
        "operationId": "cleanTaskTags",
        "responses": {
            "204": {
                "description": "Delete all associations",
                "content": {},
            },
        },
        "requestBody": {"description": "Delete all associations", "content": {}},
        "parameters": [
            {
                "name": "task_id",
                "in": "path",
                "description": "Id of the task you are looking for",
                "required": True,
                "schema": {"type": "string"},
            },
        ],
    },
}
openapi.register_path(f"{V1}/task/{{task_id}}/tags/clean", api_item)


@tasks_bp.route(f"{V1}/task/<string:task_id>/tags/clean", methods=["DELETE"])
@login_required(logger)
@rate_limited(logger=logger, hit=1, period=timedelta(seconds=1))
def task_tags_clean(task_id: str):
    """Remove all associated tags to a specific task"""

    if request.method == "DELETE":
        with current_app.sql.get_session() as session:
            task_service = TaskService(session)
            task = task_service.get_task(g.user.id, task_id)
            task_service.clean_task_tags(g.user.id, task)

            return ResponseAPI.get_response("", 204)

    else:
        return ResponseAPI.get_405_response()
