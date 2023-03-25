from flask import Flask, request, render_template, jsonify


app = Flask(__name__)


@app.route("/")
def hello():
    """Just a logo displayed to curious users"""
    return render_template("home.html")


@app.route("/tests", methods=["GET"])
def tests():
    """URL to test flask - REMOVE ME"""
    # TODO: to remove when tests are done
    return jsonify({"test_num": 456, "test_str": "test"})


@app.route("/login", methods=["POST"])
def login():
    """URL to login as an authorized user"""


@app.route("/login/2fa", methods=["POST"])
def login2fa():
    """URL to send 2FA auth - Token required"""


@app.route("/user", methods=["PUT"])
def user():
    """URL to modify user informations - Token required"""


@app.route("/tasks", methods=["GET", "POST"])
def user():
    """URL to current user tasks - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method == "POST":
        return jsonify()


@app.route("/task/<int:task_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def user(task_id):
    """URL to current user task - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method in ["PUT", "PATCH"]:
        return jsonify()
    elif request.method == "DELETE":
        return jsonify()


@app.route("/groups", methods=["GET", "POST"])
def user():
    """URL to current user groups - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method == "POST":
        return jsonify()


@app.route("/group/<int:group_id>", methods=["GET", "PUT", "PATCH", "DELETE"])
def user(group_id):
    """URL to current user group - Token required"""
    if request.method == "GET":
        return jsonify()
    elif request.method in ["PUT", "PATCH"]:
        return jsonify()
    elif request.method == "DELETE":
        return jsonify()
