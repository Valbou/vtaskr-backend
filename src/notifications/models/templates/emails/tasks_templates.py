from gettext import NullTranslations

from .base import BaseEmailTemplate

_ = NullTranslations().gettext


class TasksDailyTasksTemplate(BaseEmailTemplate):
    """Daily tasks list to do"""

    name: str = "Daily tasks list to do"
    event_name: str = "tasks:todo_today:tasks"
    subject: str = "{APP_NAME} - {nb_today} Tasks to do today"
    files_path: dict[str:str] = {
        "html": "emails/tasks/daily_todo.html",
        "txt": "emails/tasks/daily_todo.txt",
    }

    context = {
        "logo": "{EMAIL_LOGO}",
        "title": _("{nb_today} Tasks To Do Today !"),
        "content_title": _("Hi !"),
        "title_today": _("{nb_today} Tasks for Today"),
        "title_tomorrow": _("{nb_tomorrow} Tasks for Tomorrow"),
    }
