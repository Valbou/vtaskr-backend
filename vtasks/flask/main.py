from flask import Flask

from vtasks.base import base_bp
from vtasks.users import users_bp
from vtasks.tasks import tasks_bp


app = Flask(__name__)

app.register_blueprint(base_bp)
app.register_blueprint(users_bp)
app.register_blueprint(tasks_bp)
