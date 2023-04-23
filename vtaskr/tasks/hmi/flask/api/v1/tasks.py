from datetime import timedelta

from flask import current_app, g, request

from vtaskr.flask.utils import ResponseAPI
from vtaskr.redis import rate_limited
from vtaskr.tasks.hmi import TagService, TaskService
from vtaskr.tasks.hmi.dto import TagMapperDTO, TaskDTO, TaskMapperDTO
from vtaskr.tasks.persistence import TaskDB
from vtaskr.users.hmi.flask.decorators import login_required

from .. import V1, logger, openapi, tasks_bp

api_item = {
    "get": {
        "description": "Get all current user's tasks",
        "summary": "Get user's tasks",
        "operationId": "getUserTasks",
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
        "description": "Create task for the current user",
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
    """URL to current user tasks - Token required"""
    try:
        if request.method == "GET":
            with current_app.sql.get_session() as session:
                task_service = TaskService(session, current_app.testing)
                tasks = task_service.get_user_tasks(g.user.id)
                if tasks:
                    tasks_dto = TaskMapperDTO.list_models_to_list_dto(tasks)
                    return ResponseAPI.get_response(
                        TaskMapperDTO.list_dto_to_dict(tasks_dto), 200
                    )
                else:
                    return ResponseAPI.get_response([], 200)

        elif request.method == "POST":
            try:
                task_dto = TaskDTO(**request.get_json())
                task = TaskMapperDTO.dto_to_model(g.user.id, task_dto)

                with current_app.sql.get_session() as session:
                    task_db = TaskDB()
                    task_db.save(session, task)
                    task_dto = TaskMapperDTO.model_to_dto(task)
                    return ResponseAPI.get_response(
                        TaskMapperDTO.dto_to_dict(task_dto), 201
                    )
            except Exception:
                return ResponseAPI.get_error_response("Bad request", 400)

    except Exception as e:
        logger.error(str(e))
        return ResponseAPI.get_error_response("Internal error", 500)


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
    """URL to current user task - Token required"""
    with current_app.sql.get_session() as session:
        task_service = TaskService(session, current_app.testing)
        task = task_service.get_user_task(g.user.id, task_id)
        if task:
            if request.method == "GET":
                task_dto = TaskMapperDTO.model_to_dto(task)
                return ResponseAPI.get_response(
                    TaskMapperDTO.dto_to_dict(task_dto), 200
                )

            elif request.method in ("PUT", "PATCH"):
                task_dto = TaskDTO(**request.get_json())
                task = TaskMapperDTO.dto_to_model(g.user.id, task_dto, task)
                task_service.update_user_task(g.user.id, task)

                task_dto = TaskMapperDTO.model_to_dto(task)
                return ResponseAPI.get_response(
                    TaskMapperDTO.dto_to_dict(task_dto), 200
                )

            elif request.method == "DELETE":
                task_service.delete_user_task(g.user.id, task)
                return ResponseAPI.get_response({}, 204)

        else:
            return ResponseAPI.get_error_response({}, 404)


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
            task_service = TaskService(session, current_app.testing)
            task = task_service.get_user_task(g.user.id, task_id)
            if task:
                tag_service = TagService(session, current_app.testing)
                tags_dto = TagMapperDTO.list_models_to_list_dto(
                    tag_service.get_user_task_tags(g.user.id, task.id)
                )
                return ResponseAPI.get_response(
                    TaskMapperDTO.list_dto_to_dict(tags_dto), 200
                )
            else:
                return ResponseAPI.get_error_response("Task not found", 404)
    else:
        return ResponseAPI.get_error_response({}, 405)


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
    },
}
openapi.register_path(f"{V1}/task/{{task_id}}/tags/set", api_item)


@tasks_bp.route(f"{V1}/task/<string:task_id>/tags/set", methods=["PUT"])
@login_required(logger)
@rate_limited(logger=logger, hit=5, period=timedelta(seconds=1))
def task_tags_set(task_id: str):
    """Set all associated tags ids to a specific task"""

    data = request.get_json()
    tags_id = data.get("tags")
    if not isinstance(tags_id, list):
        return ResponseAPI.get_error_response("Bad request", 400)

    if request.method == "PUT":
        with current_app.sql.get_session() as session:
            task_service = TaskService(session, current_app.testing)
            task = task_service.get_user_task(g.user.id, task_id)
            try:
                task_service.set_task_tags(g.user.id, task, tags_id)
            except Exception as e:
                logger.info(str(e))
                return ResponseAPI.get_error_response("Bad request", 400)
            return ResponseAPI.get_response({}, 201)

    else:
        return ResponseAPI.get_error_response({}, 405)


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
            task_service = TaskService(session, current_app.testing)
            task = task_service.get_user_task(g.user.id, task_id)
            try:
                task_service.clean_task_tags(g.user.id, task)
            except Exception as e:
                logger.error(str(e))
                return ResponseAPI.get_error_response("Internal error", 500)
            return ResponseAPI.get_response({}, 204)

    else:
        return ResponseAPI.get_error_response({}, 405)
