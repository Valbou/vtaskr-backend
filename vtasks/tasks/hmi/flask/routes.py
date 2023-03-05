from logging import Logger
from datetime import timedelta

from flask import Blueprint, request, jsonify, current_app, g

from vtasks.flask.utils import ResponseAPI
from vtasks.redis import rate_limited
from vtasks.users.hmi.flask.decorators import login_required
from vtasks.tasks.persistence import TaskDB
from vtasks.tasks.hmi.tasks_service import TaskService
from vtasks.tasks import Task


logger = Logger(__name__)


tasks_bp = Blueprint(
    name="tasks_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


V1 = "/api/v1"


@tasks_bp.route(f"{V1}/tasks", methods=["GET", "POST"])
@login_required(logger)
@rate_limited(logger=logger, hit=1, period=timedelta(seconds=1))
def tasks():
    """URL to current user tasks - Token required"""
    try:
        if request.method == "GET":
            with current_app.sql.get_session() as session:
                task_service = TaskService(session, current_app.testing)
                data = task_service.get_user_tasks(g.user.id)
                return ResponseAPI.get_response(data, 200)

        elif request.method == "POST":
            payload: dict = request.get_json()
            try:
                task: Task = Task.from_external_data(g.user.id, payload)
                with current_app.sql.get_session() as session:
                    task_db = TaskDB()
                    task_db.save(session, task)
                    return ResponseAPI.get_response(task.to_external_data(), 201)
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


@tasks_bp.route(f"{V1}/tags", methods=["GET", "POST"])
def tags():
    """URL to current user tags - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method == "POST":
        return jsonify()


@tasks_bp.route(f"{V1}/tag/<int:group_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def tag(tag_id):
    """URL to current user tag - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method in ["PUT", "PATCH"]:
        return jsonify()
    elif request.method == "DELETE":
        return jsonify()
