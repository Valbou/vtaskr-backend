from jinja2 import FileSystemLoader

from .settings import APP_NAME


def common_data(project_dir: str) -> dict:
    return {
        "loaders": [
            FileSystemLoader(f"{project_dir}/src/{APP_NAME.lower()}/openapi/templates")
        ]
    }


def setup_celery(app, project_dir: str) -> dict:
    """Must be called only if a Celery app is needed"""

    return common_data(project_dir=project_dir)


def setup_flask(app, project_dir: str) -> dict:
    """Must be called only if a Flask app is needed"""

    return common_data(project_dir=project_dir)
