from flask import Flask

from .apps.base import base_bp
from .apps.users import users_bp
from .apps.tasks import tasks_bp


app = Flask(__name__)

app.register_blueprint(base_bp)
app.register_blueprint(users_bp)
app.register_blueprint(tasks_bp)
