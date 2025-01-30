import os

from src.libs.dependencies import DependencyInjector


class Config:
    timezone = "UTC"

    beat_sync_every = 1
    beat_max_loop_interval = 60  # Check every minute
    beat_cron_starting_deadline = 1800  # 30 minutes

    broker_connection_retry = True
    broker_connection_retry_on_startup = True

    def __init__(self, dependencies: DependencyInjector):
        self.result_backend = dependencies.cache.get_database_url()
        self.broker_url = dependencies.cache.get_database_url()

        base_log_path = os.getenv("CELERY_LOG_PATH")

        self.worker_logfile = os.path.join(base_log_path, "worker_%i.log")
        self.worker_pidfile = os.path.join(base_log_path, "worker_%i.pid")

        self.beat_logfile = os.path.join(base_log_path, "beat.log")
        self.beat_pidfile = os.path.join(base_log_path, "beat.pid")
