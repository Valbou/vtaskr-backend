from flask import Flask

from vtasks.sqlalchemy.database import SQLService
from vtasks.redis.database import NoSQLService
from vtasks.babel.translations import TranslationService
from vtasks.base.config import AVAILABLE_LANGUAGES

from vtasks.base.hmi.flask import base_bp
from vtasks.users.hmi.flask import users_bp
from vtasks.tasks.hmi.flask import tasks_bp


def create_flask_app(testing: bool = False) -> Flask:
    app = Flask(__name__)

    app.testing = testing

    app.register_blueprint(base_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)

    app.jinja_options = {"extensions": ["jinja2.ext.i18n"]}
    app.sql = SQLService(testing)
    app.nosql = NoSQLService(testing)
    app.trans = TranslationService()
    app.trans.add_domains(["users", "tasks"])
    app.trans.add_languages(list(AVAILABLE_LANGUAGES.keys()))

    return app
