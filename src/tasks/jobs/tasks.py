from celery import current_app, shared_task
from src.tasks.services import TasksService


@shared_task()
def run_dailys_tasks():
    service = TasksService(services=current_app.dependencies)
    service.send_today_tasks_notifications()
