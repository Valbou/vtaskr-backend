from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.tasks.managers import TagManager, TaskManager
from src.tasks.models import Tag, Task


class TasksService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services

        self._define_managers()

    def _define_managers(self):
        """Define managers from domain (no DI here)"""

        self.tag_manager = TagManager(services=self.services)
        self.task_manager = TaskManager(services=self.services)

    def create_new_task(self, user_id: str, task: Task) -> bool:
        """Create a new task for a user"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.create_task(
                session=session, user_id=user_id, task=task
            )

    def get_user_task(self, user_id: str, task_id: str):
        """Return a user's task"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.get_task(
                session=session, user_id=user_id, task_id=task_id
            )

    def get_user_all_tasks(self, user_id: str, qs_filters: list[Filter] | None = None):
        """Return all user's tasks"""

        with self.services.persistence.get_session() as session:
            tasks = self.task_manager.get_tasks(
                session=session, user_id=user_id, qs_filters=qs_filters
            )

        return tasks

    def get_all_tag_tasks(
        self, user_id: str, tag_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Tag]:
        """Return all tasks with this at least this tag"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.get_tag_tasks(
                session=session, user_id=user_id, tag_id=tag_id, qs_filters=qs_filters
            )

    def update_task(self, user_id: str, task: Task) -> bool:
        """Update a task"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.update_task(
                session=session, user_id=user_id, task=task
            )

    def delete_task(self, user_id: str, task: Task) -> bool:
        """Delete a task"""

        with self.services.persistence.get_session() as session:
            return self.task_manager.delete_task(
                session=session, user_id=user_id, task=task
            )

    def create_new_tag(self, user_id: str, tag: Tag) -> bool:
        """Create a new tag for a user"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.create_tag(
                session=session, user_id=user_id, tag=tag
            )

    def get_user_tag(self, user_id: str, tag_id: str) -> Tag | None:
        """Return a user's tag"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.get_tag(
                session=session, user_id=user_id, tag_id=tag_id
            )

    def check_user_tag_exists(self, user_id: str, tag_id: str) -> bool:
        """Check if user's tag exists"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.tags_exists(
                session=session, user_id=user_id, tag_ids=[tag_id]
            )

    def get_all_task_tags(self, user_id: str, task_id: str) -> list[Tag]:
        with self.services.persistence.get_session() as session:
            return self.tag_manager.get_task_tags(
                session=session, user_id=user_id, task_id=task_id
            )

    def get_tags_from_id(self, user_id: str, tag_ids: list[str]) -> list[Tag]:
        with self.services.persistence.get_session() as session:
            return self.tag_manager.get_tags_from_ids(
                session=session, user_id=user_id, tag_ids=tag_ids
            )

    def get_user_all_tags(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Tag]:
        """Return all user's tags"""

        with self.services.persistence.get_session() as session:
            tags = self.tag_manager.get_tags(
                session=session, user_id=user_id, qs_filters=qs_filters
            )

        return tags

    def update_tag(self, user_id: str, tag: Tag) -> bool:
        """Update a tag"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.update_tag(
                session=session, user_id=user_id, tag=tag
            )

    def delete_tag(self, user_id: str, tag: Tag) -> bool:
        """Delete a tag"""

        with self.services.persistence.get_session() as session:
            return self.tag_manager.delete_tag(
                session=session, user_id=user_id, tag=tag
            )

    def set_tags_to_task(self, user_id: str, task_id: str, tag_ids: list[str]) -> bool:
        """Set tags to a task"""

        with self.services.persistence.get_session() as session:
            task = self.task_manager.get_task(user_id=user_id, task_id=task_id)

            if not task:
                return False

            if tag_ids:
                tags = self.get_tags_from_id(user_id=user_id, tag_ids=tag_ids)

                if tags:
                    tags = self.tag_manager.get_tags(session=session, user_id=user_id)
                    task.tags = tags

            elif len(tag_ids) == 0:
                task.tags = []

            self.task_manager.update_task(session=session, user_id=user_id, task=task)

            return True
