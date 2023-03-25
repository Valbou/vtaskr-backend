from flask import Flask

from .apps.base import base_bp
from .apps.users import users_bp
from .apps.tasks import tasks_bp
from .database import db_session


app = Flask(__name__)


app.register_blueprint(base_bp)
app.register_blueprint(users_bp)
app.register_blueprint(tasks_bp)


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()
