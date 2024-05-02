from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions, Resources
from src.tasks.models import Task
from src.tasks.persistence import TaskDBPort
from src.tasks.settings import APP_NAME


class TaskService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.task_db: TaskDBPort = self.services.persistence.get_repository(
            APP_NAME, "Task"
        )

    def get_tasks(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[dict]:
        """Get a list of authorized tasks"""

        with self.services.persistence.get_session() as session:
            tenant_ids = self.services.identity.all_tenants_with_access(
                session,
                permission=Permissions.READ,
                user_id=user_id,
                resource=Resources.TASK,
            )

            return self.task_db.tasks(session, tenant_ids, qs_filters)

    def get_task(self, user_id: str, task_id: str) -> Task | None:
        """Get a tag if read permission was given"""

        with self.services.persistence.get_session() as session:
            task = self.task_db.load(session, task_id)

            if task:
                return (
                    task
                    if self.services.identity.can(
                        session,
                        Permissions.READ,
                        user_id,
                        task.tenant_id,
                        resource=Resources.TASK,
                    )
                    else None
                )
            return None

    def get_tag_tasks(
        self,
        user_id: str,
        tag_id: str,
        tag_tenant_id: str,
        qs_filters: list[Filter] | None = None,
    ) -> list[Task] | None:
        """Access to all tasks of one tag"""

        with self.services.persistence.get_session() as session:
            if not self.services.identity.can(
                session,
                Permissions.READ,
                user_id,
                tag_tenant_id,
                resource=Resources.TAG,
            ):
                return None

            tenant_ids = self.services.identity.all_tenants_with_access(
                session,
                permission=Permissions.READ,
                user_id=user_id,
                resource=Resources.TASK,
            )

            return self.task_db.tag_tasks(session, tenant_ids, tag_id, qs_filters)

    def set_task_tags(self, user_id: str, task: Task, tag_ids: list[str]) -> None:
        """Associate many tags to one task"""

        with self.services.persistence.get_session() as session:
            if not self.services.identity.can(
                session,
                Permissions.UPDATE,
                user_id,
                task.tenant_id,
                resource=Resources.TASK,
            ):
                return None

            tenant_ids = self.services.identity.all_tenants_with_access(
                session,
                permission=Permissions.READ,
                user_id=user_id,
                resource=Resources.TAG,
            )

            self.task_db.add_tags(session, tenant_ids, task, tag_ids)

    def save_task(self, user_id: str, task: Task) -> None:
        """Save a new task"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session,
                Permissions.CREATE,
                user_id,
                task.tenant_id,
                resource=Resources.TASK,
            ):
                self.task_db.save(session, task)

    def update_task(self, user_id: str, task: Task):
        """Update a task if update permission was given"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session,
                Permissions.UPDATE,
                user_id,
                task.tenant_id,
                resource=Resources.TASK,
            ):
                self.task_db.save(session, task)

    def clean_task_tags(self, user_id: str, task: Task):
        """Clean all tags of a task if update permission was given on task"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session,
                Permissions.UPDATE,
                user_id,
                task.tenant_id,
                resource=Resources.TASK,
            ):
                self.task_db.clean_tags(session, task)

    def delete_task(self, user_id: str, task: Task):
        """Delete a task if delete permission was given"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session,
                Permissions.DELETE,
                user_id,
                task.tenant_id,
                resource=Resources.TASK,
            ):
                self.task_db.delete(session, task)
