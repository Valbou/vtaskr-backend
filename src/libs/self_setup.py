import logging
import os
from enum import Enum
from importlib import import_module
from typing import Callable

from jinja2 import ChoiceLoader, Environment

from src.libs.dependencies import DependencyInjector
from src.settings import AVAILABLE_LANGUAGES, INSTALLED_APPS, SECRET_KEY

logger = logging.getLogger(__name__)


class AppTypes(Enum):
    FLASK = "flask"
    FASTAPI = "fastapi"
    CELERY = "celery"


def app_setup(app, app_type: AppTypes, dependencies: DependencyInjector):
    """Add dependencies to a given app"""

    app.secret_key = SECRET_KEY
    app.dependencies = dependencies

    project_dir = os.getcwd()

    app.static_folder = f"{project_dir}/src/static"

    # App self config
    loaders = []
    domains: list[str] = []
    repositories: list[tuple] = []
    observers: list = []
    permissions_resources: list[str] = []

    for module in INSTALLED_APPS:
        logger.info(f"loading app {module}")

        setup_app: Callable = getattr(
            import_module(f"src.{module}.config"), f"setup_{app_type.value}"
        )
        result = setup_app(app=app, project_dir=project_dir)

        loaders.extend(result.get("loaders", []))
        domains.extend(result.get("domains", []))
        repositories.extend(result.get("repositories", []))
        observers.extend(result.get("observers", []))
        permissions_resources.extend(result.get("permissions_resources", []))

        logger.info(f"app {module} ready.")

    logger.info("loading Jinja items")

    app.jinja_env = Environment(autoescape=True)
    app.jinja_env.add_extension("jinja2.ext.i18n")
    app.jinja_env.loader = ChoiceLoader(loaders)

    logger.info("set up dependencies.")

    app.dependencies.instantiate_dependencies()
    app.dependencies.set_context(
        app=app,
        domains=domains,
        languages=list(AVAILABLE_LANGUAGES.keys()),
        repositories=repositories,
        observers=observers,
        permissions_resources=permissions_resources,
    )
