import os

from jinja2 import ChoiceLoader, FileSystemLoader

from flask import Flask
from src.base.hmi.flask import base_bp
from src.libs.babel.translations import TranslationService
from src.libs.eventbus.register import *  # noqa E401 F403
from src.settings import AVAILABLE_LANGUAGES
from src.tasks.hmi.flask.api import tasks_bp
from src.users.hmi.flask.api import users_bp


def create_flask_app(
    sql_class, nosql_class, notification_class, eventbus_class
) -> Flask:
    app = Flask(__name__)

    app.register_blueprint(base_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)

    project_dir = os.getcwd()

    app.static_folder = f"{project_dir}/src/static"

    app.jinja_env.add_extension("jinja2.ext.i18n")
    app.jinja_env.loader = ChoiceLoader(
        [
            FileSystemLoader(f"{project_dir}/src/base/hmi/flask/templates"),
            FileSystemLoader(f"{project_dir}/src/users/hmi/flask/templates"),
            FileSystemLoader(f"{project_dir}/src/tasks/hmi/flask/templates"),
            FileSystemLoader(f"{project_dir}/src/libs/openapi/templates"),
        ]
    )

    app.sql = sql_class()
    app.nosql = nosql_class()
    app.notification = notification_class()
    app.eventbus = eventbus_class(app_ctx=app)

    app.trans = TranslationService()
    app.trans.add_domains(["users", "tasks"])
    app.trans.add_languages(list(AVAILABLE_LANGUAGES.keys()))

    return app
