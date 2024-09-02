from src.libs.dependencies import DependencyInjector
from src.libs.hmi.querystring import Filter
from src.libs.iam.constants import Permissions
from src.tasks.models import Tag
from src.tasks.persistence import TagDBPort
from src.tasks.settings import APP_NAME


class TagManager:
    def __init__(self, services: DependencyInjector) -> None:
        self.services = services
        self.tag_db: TagDBPort = self.services.persistence.get_repository(
            APP_NAME, "Tag"
        )

    def create_tag(self, session, user_id: str, tag: Tag) -> bool:
        """Create a new tag"""

        if self.services.identity.can(
            session,
            Permissions.CREATE,
            user_id,
            tag.tenant_id,
            resource="Task",
        ):
            self.tag_db.save(session, tag)

            return True

        return False

    def tags_exists(self, session, user_id: str, tag_ids: list[str]) -> bool:
        """Check if tag exists"""

        tenant_ids = self.services.identity.all_tenants_with_access(
            session,
            permission=Permissions.READ,
            user_id=user_id,
            resource="Tag",
        )

        return self.tag_db.all_exists(
            session=session, tenant_ids=tenant_ids, ids=tag_ids
        )

    def get_tag(self, session, user_id: str, tag_id: str) -> Tag | None:
        """Get a tag if read permission was given"""

        tag = self.tag_db.load(session, tag_id)

        if tag:
            return (
                tag
                if self.services.identity.can(
                    session,
                    Permissions.READ,
                    user_id,
                    tag.tenant_id,
                    resource="Tag",
                )
                else None
            )

        return None

    def get_tags(
        self, session, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[Tag]:
        """Get a list of authorized tags"""

        tenant_ids = self.services.identity.all_tenants_with_access(
            session,
            permission=Permissions.READ,
            user_id=user_id,
            resource="Tag",
        )

        return self.tag_db.tags(session, tenant_ids, qs_filters)

    def get_tags_from_ids(self, session, user_id: str, tag_ids: list[str]) -> list[Tag]:
        """Get a list of authorized tags from the list"""

        tenant_ids = self.services.identity.all_tenants_with_access(
            session,
            permission=Permissions.READ,
            user_id=user_id,
            resource="Tag",
        )

        return self.tag_db.tags_from_ids(session, tenant_ids, tag_ids)

    def get_task_tags(self, session, user_id: str, task_id: str) -> list[Tag] | None:
        """Access to all tags of one task"""

        tenant_ids = self.services.identity.all_tenants_with_access(
            session,
            permission=Permissions.READ,
            user_id=user_id,
            resource="Task",
        )

        return self.tag_db.task_tags(
            session=session, tenant_ids=tenant_ids, task_id=task_id
        )

    def update_tag(self, session, user_id: str, tag: Tag) -> bool:
        """Update a tag if update permission was given"""

        if self.services.identity.can(
            session,
            Permissions.UPDATE,
            user_id,
            tag.tenant_id,
            resource="Tag",
        ):
            self.tag_db.save(session, tag)

            return True

        return False

    def delete_tag(self, session, user_id: str, tag: Tag):
        """Delete a tag if delete permission was given"""

        if self.services.identity.can(
            session,
            Permissions.DELETE,
            user_id,
            tag.tenant_id,
            resource="Tag",
        ):
            self.tag_db.delete(session, tag)

            return True

        return False
