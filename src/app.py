from flask import Flask, request, render_template, jsonify

from .apps.users import users_bp
from .apps.tasks import tasks_bp


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


app.register_blueprint(users_bp)
app.register_blueprint(tasks_bp)
