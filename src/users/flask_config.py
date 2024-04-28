from jinja2 import FileSystemLoader

from flask import Flask
from src.users.hmi.flask import users_bp

APP_NAME = "users"


def setup_flask(app: Flask, project_dir: str) -> dict:
    app.register_blueprint(users_bp)

    return {
        "domains": [APP_NAME.lower()],
        "loaders": [
            FileSystemLoader(
                f"{project_dir}/src/{APP_NAME.lower()}/hmi/flask/templates"
            )
        ],
    }
