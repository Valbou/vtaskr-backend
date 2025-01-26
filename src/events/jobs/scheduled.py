from celery import Celery
from celery.schedules import crontab


def schedule_tasks(app: Celery):
    app.conf.beat_schedule["celery-health-check"] = {
        "task": "src.events.jobs.tasks.celery_health_check",
        "schedule": crontab(minute=0),
    }
