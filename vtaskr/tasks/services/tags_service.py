from sqlalchemy.orm import Session

from vtaskr.libs.flask.querystring import Filter
from vtaskr.libs.iam.config import PermissionControl
from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.tasks.models import Tag
from vtaskr.tasks.persistence import TagDB


class TagService:
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.tag_db = TagDB()
        self.control = PermissionControl(self.session)

    def get_tags(
        self, user_id: str, qs_filters: list[Filter] | None = None
    ) -> list[dict]:
        """Get a list of authorized tags"""

        tenant_ids = self.control.all_tenants_with_access(
            permission=Permissions.READ, user_id=user_id, resource=Resources.TAG
        )

        return self.tag_db.tags(self.session, tenant_ids, qs_filters)

    def get_tag(self, user_id: str, tag_id: str) -> Tag | None:
        """Get a tag if read permission was given"""

        tag = self.tag_db.load(self.session, tag_id)

        if tag:
            return (
                tag
                if self.control.can(
                    Permissions.READ, user_id, tag.tenant_id, resource=Resources.TAG
                )
                else None
            )
        return None

    def get_task_tags(
        self, user_id: str, task_id: str, task_tenant_id: str
    ) -> list[Tag] | None:
        """Access to all tags of one task"""

        if not self.control.can(
            Permissions.READ, user_id, task_tenant_id, resource=Resources.TASK
        ):
            return None

        tenant_ids = self.control.all_tenants_with_access(
            permission=Permissions.READ,
            user_id=user_id,
            resource=Resources.TAG,
        )

        return self.tag_db.task_tags(self.session, tenant_ids, task_id)

    def save_tag(self, user_id: str, tag: Tag) -> None:
        """Save a new tag"""

        if self.control.can(
            Permissions.CREATE, user_id, tag.tenant_id, resource=Resources.TAG
        ):
            self.tag_db.save(self.session, tag)

    def update_tag(self, user_id: str, tag: Tag):
        """Update a tag if update permission was given"""

        if self.control.can(
            Permissions.UPDATE, user_id, tag.tenant_id, resource=Resources.TAG
        ):
            self.tag_db.save(self.session, tag)

    def delete_tag(self, user_id: str, tag: Tag):
        """Delete a tag if delete permission was given"""

        if self.control.can(
            Permissions.DELETE, user_id, tag.tenant_id, resource=Resources.TAG
        ):
            self.tag_db.delete(self.session, tag)
