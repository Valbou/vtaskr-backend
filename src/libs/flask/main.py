import logging

from flask import Flask
from src.libs.dependencies import DependencyInjector
from src.libs.self_setup import AppTypes, app_setup
from src.settings import APP_NAME

logger = logging.getLogger(__name__)


def create_flask_app(dependencies: DependencyInjector) -> Flask:
    logger.info(f"Starting Flask {APP_NAME}...")

    app = Flask(__name__)
    app_setup(app=app, app_type=AppTypes.FLASK, dependencies=dependencies)

    logger.info(f"{APP_NAME} ready !")

    return app
