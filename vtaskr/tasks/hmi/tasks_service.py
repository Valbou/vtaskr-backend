from typing import List, Optional

from sqlalchemy.orm import Session

from vtaskr.libs.flask.querystring import Filter
from vtaskr.tasks.hmi.ports import AbstractTaskPort
from vtaskr.tasks.models import Task
from vtaskr.tasks.persistence import TaskDB
from vtaskr.users import PermissionControl


class TaskService(AbstractTaskPort):
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.task_db = TaskDB()
        self.control = PermissionControl()

    def get_user_tasks(
        self, user_id: str, qs_filters: Optional[List[Filter]] = None
    ) -> List[dict]:
        return self.task_db.user_tasks(self.session, user_id, qs_filters)

    def get_user_task(self, user_id: str, task_id: str) -> Optional[Task]:
        task = self.task_db.load(self.session, task_id)
        return task if self.control.is_owner(user_id, task.user_id) else None

    def get_user_tag_tasks(
        self, user_id: str, tag_id: str, qs_filters: Optional[List[Filter]] = None
    ) -> List[Task]:
        return self.task_db.user_tag_tasks(self.session, user_id, tag_id, qs_filters)

    def set_task_tags(self, user_id: str, task: Task, tags_id: List[str]):
        if self.control.is_owner(user_id, task.user_id):
            self.task_db.user_add_tags(self.session, user_id, task, tags_id)

    def update_user_task(self, user_id: str, task: Task):
        if self.control.is_owner(user_id, task.user_id):
            self.task_db.save(self.session, task)

    def clean_task_tags(self, user_id: str, task: Task):
        if self.control.is_owner(user_id, task.user_id):
            self.task_db.clean_tags(self.session, user_id, task)

    def delete_user_task(self, user_id: str, task: Task):
        if self.control.is_owner(user_id, task.user_id):
            self.task_db.delete(self.session, task)
