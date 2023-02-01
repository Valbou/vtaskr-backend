from flask import Blueprint, request, jsonify


tasks_bp = Blueprint(
    name="tasks_bp",
    import_name=__name__,
    static_folder="static",
    template_folder="templates",
)


@tasks_bp.route("/tasks", methods=["GET", "POST"])
def tasks():
    """URL to current user tasks - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method == "POST":
        return jsonify()


@tasks_bp.route("/task/<int:task_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def task(task_id):
    """URL to current user task - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method in ["PUT", "PATCH"]:
        return jsonify()
    elif request.method == "DELETE":
        return jsonify()


@tasks_bp.route("/groups", methods=["GET", "POST"])
def groups():
    """URL to current user groups - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method == "POST":
        return jsonify()


@tasks_bp.route("/group/<int:group_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def group(group_id):
    """URL to current user group - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method in ["PUT", "PATCH"]:
        return jsonify()
    elif request.method == "DELETE":
        return jsonify()
