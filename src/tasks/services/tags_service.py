from src.libs.dependencies import DependencyInjector
from src.libs.flask.querystring import Filter
from src.libs.iam.constants import Permissions, Resources
from src.tasks.models import Tag
from src.tasks.persistence import TagDBPort
from src.tasks.settings import APP_NAME


class TagService:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.tag_db: TagDBPort = self.services.persistence.get_repository(
            APP_NAME, "Tag"
        )

    def get_tags(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[dict]:
        """Get a list of authorized tags"""

        with self.services.persistence.get_session() as session:
            tenant_ids = self.services.identity.all_tenants_with_access(
                session,
                permission=Permissions.READ,
                user_id=user_id,
                resource=Resources.TAG,
            )

            return self.tag_db.tags(session, tenant_ids, qs_filters)

    def get_tag(self, user_id: str, tag_id: str) -> Tag | None:
        """Get a tag if read permission was given"""

        with self.services.persistence.get_session() as session:
            tag = self.tag_db.load(session, tag_id)

            if tag:
                return (
                    tag
                    if self.services.identity.can(
                        session,
                        Permissions.READ,
                        user_id,
                        tag.tenant_id,
                        resource=Resources.TAG,
                    )
                    else None
                )
        return None

    def get_task_tags(
        self, user_id: str, task_id: str, task_tenant_id: str
    ) -> list[Tag] | None:
        """Access to all tags of one task"""

        with self.services.persistence.get_session() as session:
            if not self.services.identity.can(
                session,
                Permissions.READ,
                user_id,
                task_tenant_id,
                resource=Resources.TASK,
            ):
                return None

            tenant_ids = self.services.identity.all_tenants_with_access(
                session,
                permission=Permissions.READ,
                user_id=user_id,
                resource=Resources.TAG,
            )

            return self.tag_db.task_tags(session, tenant_ids, task_id)

    def save_tag(self, user_id: str, tag: Tag) -> None:
        """Save a new tag"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session,
                Permissions.CREATE,
                user_id,
                tag.tenant_id,
                resource=Resources.TAG,
            ):
                self.tag_db.save(session, tag)

    def update_tag(self, user_id: str, tag: Tag):
        """Update a tag if update permission was given"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session,
                Permissions.UPDATE,
                user_id,
                tag.tenant_id,
                resource=Resources.TAG,
            ):
                self.tag_db.save(session, tag)

    def delete_tag(self, user_id: str, tag: Tag):
        """Delete a tag if delete permission was given"""

        with self.services.persistence.get_session() as session:
            if self.services.identity.can(
                session,
                Permissions.DELETE,
                user_id,
                tag.tenant_id,
                resource=Resources.TAG,
            ):
                self.tag_db.delete(session, tag)
