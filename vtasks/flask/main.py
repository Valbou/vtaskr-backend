import os

from flask import Flask
from jinja2 import FileSystemLoader, ChoiceLoader

from vtasks.babel.translations import TranslationService
from vtasks.base.config import AVAILABLE_LANGUAGES
from vtasks.base.hmi.flask import base_bp
from vtasks.redis.database import NoSQLService
from vtasks.sqlalchemy.database import SQLService
from vtasks.tasks.hmi.flask.api import tasks_bp
from vtasks.users.hmi.flask.api import users_bp


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
            FileSystemLoader(f"{project_dir}/vtasks/base/hmi/flask/templates"),
            FileSystemLoader(f"{project_dir}/vtasks/users/hmi/flask/templates"),
            FileSystemLoader(f"{project_dir}/vtasks/tasks/hmi/flask/templates"),
        ]
    )
    app.sql = SQLService(testing)
    app.nosql = NoSQLService(testing)

    app.trans = TranslationService()
    app.trans.add_domains(["users", "tasks"])
    app.trans.add_languages(list(AVAILABLE_LANGUAGES.keys()))

    return app
