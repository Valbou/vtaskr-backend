from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.libs.flask.querystring import Filter
from vtaskr.libs.iam.config import PermissionControl
from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.tasks.hmi.ports import AbstractTaskPort
from vtaskr.tasks.models import Task
from vtaskr.tasks.persistence import TaskDB


class TaskService(AbstractTaskPort):
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.task_db = TaskDB()
        self.control = PermissionControl(self.session, resource=Resources.TASK)

    def get_tenant_tasks(
        self, tenant_id: str, qs_filters: Optional[list[Filter]] = None
    ) -> list[dict]:
        return self.task_db.tenant_tasks(self.session, tenant_id, qs_filters)

    def get_tenant_task(self, tenant_id: str, task_id: str) -> Optional[Task]:
        task = self.task_db.load(self.session, task_id)
        return (
            task
            if self.control.can(Permissions.READ, tenant_id, task.tenant_id)
            else None
        )

    def get_tenant_tag_tasks(
        self, tenant_id: str, tag_id: str, qs_filters: Optional[list[Filter]] = None
    ) -> list[Task]:
        return self.task_db.tenant_tag_tasks(
            self.session, tenant_id, tag_id, qs_filters
        )

    def set_task_tags(self, tenant_id: str, task: Task, tags_id: list[str]):
        if self.control.can(Permissions.UPDATE, tenant_id, task.tenant_id):
            self.task_db.tenant_add_tags(self.session, tenant_id, task, tags_id)

    def update_tenant_task(self, tenant_id: str, task: Task):
        if self.control.can(Permissions.UPDATE, tenant_id, task.tenant_id):
            self.task_db.save(self.session, task)

    def clean_task_tags(self, tenant_id: str, task: Task):
        if self.control.can(Permissions.UPDATE, tenant_id, task.tenant_id):
            self.task_db.clean_tags(self.session, tenant_id, task)

    def delete_tenant_task(self, tenant_id: str, task: Task):
        if self.control.can(Permissions.DELETE, tenant_id, task.tenant_id):
            self.task_db.delete(self.session, task)
