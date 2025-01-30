from celery import Celery
from celery.schedules import crontab


def schedule_tasks(app: Celery):
    app.conf.beat_schedule["dailys-notify-tasks"] = {
        "task": "src.tasks.jobs.tasks.run_daily_tasks",
        "schedule": crontab(hour=0, minute=0),
    }
