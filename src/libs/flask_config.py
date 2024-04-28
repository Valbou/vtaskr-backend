from jinja2 import FileSystemLoader

from flask import Flask

APP_NAME = "libs"


def setup_flask(app: Flask, project_dir: str) -> dict:
    return {
        "loaders": [
            FileSystemLoader(f"{project_dir}/src/{APP_NAME.lower()}/openapi/templates")
        ]
    }
