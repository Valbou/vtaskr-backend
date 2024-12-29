import logging

from celery import Celery
from src.libs.dependencies import DependencyInjector
from src.libs.self_setup import AppTypes, app_setup
from src.settings import APP_NAME

logger = logging.getLogger(__name__)


def create_celery_app(dependencies: DependencyInjector) -> Celery:
    logger.info(f"Starting Celery {APP_NAME}...")

    app = Celery(__name__)
    app.conf.timezone = "UTC"
    app_setup(app=app, app_type=AppTypes.CELERY, dependencies=dependencies)
    app.conf.broker_url = app.dependencies.cache.get_database_url()

    logger.info(f"{APP_NAME} ready !")

    return app
