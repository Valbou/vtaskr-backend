from datetime import timedelta

from flask import current_app, g, jsonify, request

from vtasks.flask.utils import ResponseAPI
from vtasks.redis import rate_limited
from vtasks.tasks.hmi.dto import TaskDTO, TaskMapperDTO
from vtasks.tasks.hmi.tasks_service import TaskService
from vtasks.tasks.persistence import TaskDB
from vtasks.users.hmi.flask.decorators import login_required

from .. import V1, logger, tasks_bp


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


@tasks_bp.route(f"{V1}/task/<int:task_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def task(task_id):
    """URL to current user task - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method in ["PUT", "PATCH"]:
        return jsonify()
    elif request.method == "DELETE":
        return jsonify()
