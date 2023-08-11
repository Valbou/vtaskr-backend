from typing import List, Optional

from sqlalchemy.orm import Session

from vtaskr.libs.flask.querystring import Filter
from vtaskr.tasks.models import Tag
from vtaskr.tasks.persistence.ports import AbstractTagPort
from vtaskr.tasks.persistence.sqlalchemy.querysets import TagQueryset


class TagDB(AbstractTagPort):
    def __init__(self) -> None:
        super().__init__()
        self.tag_qs = TagQueryset()

    def load(self, session: Session, id: str) -> Optional[Tag]:
        self.tag_qs.id(id)
        result = session.scalars(self.tag_qs.statement).one_or_none()
        return result

    def save(self, session: Session, tag: Tag, autocommit: bool = True):
        session.add(tag)
        if autocommit:
            session.commit()

    def delete(self, session: Session, tag: Tag, autocommit: bool = True):
        session.delete(tag)
        if autocommit:
            session.commit()

    def exists(self, session: Session, id: str) -> bool:
        self.tag_qs.id(id)
        return session.query(self.tag_qs.statement.exists()).scalar()

    def user_tags(
        self, session: Session, user_id: str, filters: Optional[List[Filter]] = None
    ) -> List[Tag]:
        """Retrieve all user's tags"""

        filters = filters or []
        if filters:
            self.tag_qs.from_filters(filters)

        self.tag_qs.user(user_id)
        return session.execute(self.tag_qs.statement).scalars().all()

    def user_task_tags(
        self,
        session: Session,
        user_id: str,
        task_id: str,
        filters: Optional[List[Filter]] = None,
    ) -> List[Tag]:
        """Retrieve all user's tags for this task"""

        filters = filters or []
        if filters:
            self.tag_qs.from_filters(filters)

        self.tag_qs.user(user_id).task(task_id)
        return session.execute(self.tag_qs.statement).scalars().all()
