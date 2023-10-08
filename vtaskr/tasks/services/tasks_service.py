from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.libs.flask.querystring import Filter
from vtaskr.libs.iam.config import PermissionControl
from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.tasks.models import Task
from vtaskr.tasks.persistence import TaskDB


class TaskService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.task_db = TaskDB()
        self.control = PermissionControl(self.session)

    def get_tasks(
        self, user_id: str, qs_filters: Optional[list[Filter]] = None
    ) -> list[dict]:
        """Get a list of authorized tasks"""

        tenant_ids = self.control.all_tenants_with_access(
            permission=Permissions.READ, user_id=user_id, resource=Resources.TASK
        )

        return self.task_db.tasks(self.session, tenant_ids, qs_filters)

    def get_task(self, user_id: str, task_id: str) -> Optional[Task]:
        """Get a tag if read permission was given"""

        task = self.task_db.load(self.session, task_id)

        return (
            task
            if self.control.can(
                Permissions.READ, user_id, task.tenant_id, resource=Resources.TASK
            )
            else None
        )

    def get_tag_tasks(
        self,
        user_id: str,
        tag_id: str,
        tag_tenant_id: str,
        qs_filters: Optional[list[Filter]] = None,
    ) -> list[Task] | None:
        """Access to all tasks of one tag"""

        if not self.control.can(
            Permissions.READ, user_id, tag_tenant_id, resource=Resources.TAG
        ):
            return None

        tenant_ids = self.control.all_tenants_with_access(
            permission=Permissions.READ,
            user_id=user_id,
            resource=Resources.TASK,
        )

        return self.task_db.tag_tasks(self.session, tenant_ids, tag_id, qs_filters)

    def set_task_tags(self, user_id: str, task: Task, tag_ids: list[str]) -> None:
        """Associate many tags to one task"""
        if not self.control.can(
            Permissions.UPDATE, user_id, task.tenant_id, resource=Resources.TASK
        ):
            return None

        tenant_ids = self.control.all_tenants_with_access(
            permission=Permissions.READ,
            user_id=user_id,
            resource=Resources.TAG,
        )

        self.task_db.add_tags(self.session, tenant_ids, task, tag_ids)

    def save_task(self, user_id: str, task: Task) -> None:
        """Save a new task"""
        if self.control.can(
            Permissions.CREATE, user_id, task.tenant_id, resource=Resources.TASK
        ):
            self.task_db.save(self.session, task)

    def update_task(self, user_id: str, task: Task):
        """Update a task if update permission was given"""
        if self.control.can(
            Permissions.UPDATE, user_id, task.tenant_id, resource=Resources.TASK
        ):
            self.task_db.save(self.session, task)

    def clean_task_tags(self, user_id: str, task: Task):
        """Clean all tags of a task if update permission was given on task"""
        if self.control.can(
            Permissions.UPDATE, user_id, task.tenant_id, resource=Resources.TASK
        ):
            self.task_db.clean_tags(self.session, task)

    def delete_task(self, user_id: str, task: Task):
        """Delete a task if delete permission was given"""
        if self.control.can(
            Permissions.DELETE, user_id, task.tenant_id, resource=Resources.TASK
        ):
            self.task_db.delete(self.session, task)
