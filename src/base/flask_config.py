from jinja2 import FileSystemLoader

from flask import Flask
from src.base.hmi.flask import base_bp

from .settings import APP_NAME


def setup_flask(app: Flask, project_dir: str) -> dict:
    app.register_blueprint(base_bp)

    return {
        "loaders": [
            FileSystemLoader(
                f"{project_dir}/src/{APP_NAME.lower()}/hmi/flask/templates"
            )
        ]
    }
