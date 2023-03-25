from typing import List, Optional

from sqlalchemy.orm import Session
from vtasks.tasks.hmi.ports import AbstractTaskPort
from vtasks.tasks.models import Task
from vtasks.tasks.persistence import TaskDB
from vtasks.users import PermissionControl


class TaskService(AbstractTaskPort):
    def __init__(self, session: Session, testing: bool = False) -> None:
        self.session: Session = session
        self.task_db = TaskDB()
        self.control = PermissionControl()

    def get_user_tasks(self, user_id: str) -> List[dict]:
        return self.task_db.user_tasks(self.session, user_id)

    def get_user_task(self, user_id: str, task_id: str) -> Optional[Task]:
        task = self.task_db.load(self.session, task_id)
        return task if self.control.is_owner(user_id, task.user_id) else None

    def update_user_task(self, user_id: str, task: Task):
        if self.control.is_owner(user_id, task.user_id):
            self.task_db.save(self.session, task)

    def delete_user_task(self, user_id: str, task: Task):
        if self.control.is_owner(user_id, task.user_id):
            self.task_db.delete(self.session, task)
