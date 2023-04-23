from typing import List, Optional

from sqlalchemy.orm import Session

from vtaskr.tasks.hmi.ports import AbstractTagPort
from vtaskr.tasks.models import Tag
from vtaskr.tasks.persistence import TagDB
from vtaskr.users import PermissionControl


class TagService(AbstractTagPort):
    def __init__(self, session: Session, testing: bool = False) -> None:
        self.session: Session = session
        self.tag_db = TagDB()
        self.control = PermissionControl()

    def get_user_tags(self, user_id: str) -> List[dict]:
        return self.tag_db.user_tags(self.session, user_id)

    def get_user_tag(self, user_id: str, tag_id: str) -> Optional[Tag]:
        tag = self.tag_db.load(self.session, tag_id)
        return tag if self.control.is_owner(user_id, tag.user_id) else None

    def get_user_task_tags(self, user_id: str, task_id: str) -> List[Tag]:
        return self.tag_db.user_task_tags(self.session, user_id, task_id)

    def update_user_tag(self, user_id: str, tag: Tag):
        if self.control.is_owner(user_id, tag.user_id):
            self.tag_db.save(self.session, tag)

    def delete_user_tag(self, user_id: str, tag: Tag):
        if self.control.is_owner(user_id, tag.user_id):
            self.tag_db.delete(self.session, tag)
