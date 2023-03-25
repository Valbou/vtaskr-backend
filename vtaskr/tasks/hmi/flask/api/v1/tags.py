from flask import jsonify, request

from .. import V1, tasks_bp


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
