from typing import Optional

from sqlalchemy.orm import Session

from vtaskr.libs.iam.config import PermissionControl
from vtaskr.libs.iam.constants import Permissions, Resources
from vtaskr.tasks.hmi.ports import AbstractTagPort
from vtaskr.tasks.models import Tag
from vtaskr.tasks.persistence import TagDB


class TagService(AbstractTagPort):
    def __init__(self, session: Session) -> None:
        self.session: Session = session
        self.tag_db = TagDB()
        self.control = PermissionControl(self.session, resource=Resources.TAG)

    def get_tenant_tags(self, tenant_id: str) -> list[dict]:
        return self.tag_db.tenant_tags(self.session, tenant_id)

    def get_tenant_tag(self, tenant_id: str, tag_id: str) -> Optional[Tag]:
        tag = self.tag_db.load(self.session, tag_id)
        return (
            tag
            if self.control.can(Permissions.READ, tenant_id, tag.tenant_id)
            else None
        )

    def get_tenant_task_tags(self, tenant_id: str, task_id: str) -> list[Tag]:
        return self.tag_db.tenant_task_tags(self.session, tenant_id, task_id)

    def update_tenant_tag(self, tenant_id: str, tag: Tag):
        if self.control.can(Permissions.UPDATE, tenant_id, tag.tenant_id):
            self.tag_db.save(self.session, tag)

    def delete_tenant_tag(self, tenant_id: str, tag: Tag):
        if self.control.can(Permissions.DELETE, tenant_id, tag.tenant_id):
            self.tag_db.delete(self.session, tag)
