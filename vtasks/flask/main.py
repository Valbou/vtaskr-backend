import os
from flask import Flask

from vtasks.sqlalchemy.database import SQLService

from vtasks.base.http.flask import base_bp
from vtasks.users.http.flask import users_bp
from vtasks.tasks.http.flask import tasks_bp


def create_flask_app(testing: bool = False):
    app = Flask(__name__)

    app.testing = testing

    app.register_blueprint(base_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(tasks_bp)

    app.jinja_options = {"extensions": ['jinja2.ext.i18n']}
    app.sql_service = SQLService(testing)
    app.timezone = os.getenv("TIMEZONE", "Europe/Paris")
    app.locale = os.getenv("LOCALE", "fr_FR")

    return app
