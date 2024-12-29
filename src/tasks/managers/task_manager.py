from datetime import datetime

from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions
from src.tasks.models import Task
from src.tasks.persistence import TaskDBPort
from src.tasks.settings import APP_NAME


class TaskManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.task_db: TaskDBPort = self.services.persistence.get_repository(
            APP_NAME, "Task"
        )

    def create_task(self, session, user_id: str, task: Task) -> bool:
        """Save a new task"""

        if self.services.identity.can(
            session,
            Permissions.CREATE,
            user_id,
            task.tenant_id,
            resource="Task",
        ):
            self.task_db.save(session, task)

            return True

        return False

    def get_task(self, session, user_id: str, task_id: str) -> Task | None:
        """Get a task if read permission was given"""

        task = self.task_db.load(session, task_id)

        if task:
            return (
                task
                if self.services.identity.can(
                    session,
                    Permissions.READ,
                    user_id,
                    task.tenant_id,
                    resource="Task",
                )
                else None
            )
        return None

    def get_tasks(
        self, session, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[dict]:
        """Get a list of authorized tasks"""

        tenant_ids = self.services.identity.all_tenants_with_access(
            session,
            permission=Permissions.READ,
            user_id=user_id,
            resource="Task",
        )

        return self.task_db.tasks(session, tenant_ids, qs_filters)

    def get_tag_tasks(
        self,
        session,
        user_id: str,
        tag_id: str,
        qs_filters: list[Filter] | None = None,
    ) -> list[Task] | None:
        """Access to all tasks of one tag"""

        tenant_ids = self.services.identity.all_tenants_with_access(
            session,
            permission=Permissions.READ,
            user_id=user_id,
            resource="Task",
        )

        return self.task_db.tag_tasks(
            session=session, tenant_ids=tenant_ids, tag_id=tag_id, qs_filters=qs_filters
        )

    def update_task(self, session, user_id: str, task: Task) -> bool:
        """Update a task if update permission was given"""

        if self.services.identity.can(
            session,
            Permissions.UPDATE,
            user_id,
            task.tenant_id,
            resource="Task",
        ):
            self.task_db.save(session, task)

            return True

        return False

    def clean_task_tags(self, session, user_id: str, task: Task) -> bool:
        """Clean all tags of a task if update permission was given on task"""

        if self.services.identity.can(
            session,
            Permissions.UPDATE,
            user_id,
            task.tenant_id,
            resource="Task",
        ):
            self.task_db.clean_tags(session, task)

            return True

        return False

    def delete_task(self, session, user_id: str, task: Task) -> bool:
        """Delete a task if delete permission was given"""

        if self.services.identity.can(
            session,
            Permissions.DELETE,
            user_id,
            task.tenant_id,
            resource="Task",
        ):
            self.task_db.delete(session, task)

            return True

        return False

    def delete_all_tenant_tasks(self, session, tenant_id: str) -> None:
        self.task_db.delete_all_by_tenant(session=session, tenant_id=tenant_id)

    def all_assigned_to_for_scheduled_between(
        self, session, start: datetime, end: datetime
    ) -> list[str]:
        """Return a list of assigned_to for a period"""

        return self.task_db.all_assigned_to_for_scheduled_between(
            session=session, start=start, end=end
        )

    def get_tasks_assigned_to_and_scheduled_between(
        self, session, ids: list[str], start: datetime, end: datetime
    ) -> list[Task]:
        """Return all tasks assigned to for a period"""

        return self.task_db.get_tasks_assigned_to_and_scheduled_between(
            session=session, ids=ids, start=start, end=end
        )
