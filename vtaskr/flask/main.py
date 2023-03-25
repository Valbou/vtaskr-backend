import os

from flask import Flask
from jinja2 import ChoiceLoader, FileSystemLoader

from vtaskr.babel.translations import TranslationService
from vtaskr.base.config import AVAILABLE_LANGUAGES
from vtaskr.base.hmi.flask import base_bp
from vtaskr.redis.database import NoSQLService
from vtaskr.sqlalchemy.database import SQLService
from vtaskr.tasks.hmi.flask.api import tasks_bp
from vtaskr.users.hmi.flask.api import users_bp


def create_flask_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    app.testing = testing

    app.register_blueprint(base_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)

    app.jinja_env.add_extension("jinja2.ext.i18n")

    project_dir = os.getcwd()
    app.jinja_env.loader = ChoiceLoader(
        [
            FileSystemLoader(f"{project_dir}/vtaskr/base/hmi/flask/templates"),
            FileSystemLoader(f"{project_dir}/vtaskr/users/hmi/flask/templates"),
            FileSystemLoader(f"{project_dir}/vtaskr/tasks/hmi/flask/templates"),
        ]
    )
    app.sql = SQLService(testing)
    app.nosql = NoSQLService(testing)

    app.trans = TranslationService()
    app.trans.add_domains(["users", "tasks"])
    app.trans.add_languages(list(AVAILABLE_LANGUAGES.keys()))

    return app
