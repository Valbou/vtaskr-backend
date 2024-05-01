import os
from importlib import import_module
from typing import Callable

from jinja2 import ChoiceLoader

from flask import Flask
from src.libs.dependencies import DependencyInjector
from src.settings import AVAILABLE_LANGUAGES, INSTALLED_APPS


def create_flask_app(dependencies: DependencyInjector) -> Flask:
    app = Flask(__name__)

    project_dir = os.getcwd()

    app.static_folder = f"{project_dir}/src/static"

    # App self config
    loaders = []
    domains: list[str] = []
    for module in INSTALLED_APPS:
        setup_app: Callable = getattr(
            import_module(f"src.{module}.flask_config"), "setup_flask"
        )
        result = setup_app(app=app, project_dir=project_dir)
        loaders.extend(result.get("loaders", []))
        domains.extend(result.get("domains", []))

    app.jinja_env.add_extension("jinja2.ext.i18n")
    app.jinja_env.loader = ChoiceLoader(loaders)

    dependencies.instantiate_dependencies()
    dependencies.set_context(
        app=app, domains=domains, languages=list(AVAILABLE_LANGUAGES.keys())
    )
    app.dependencies = dependencies

    return app
