from datetime import datetime
from zoneinfo import ZoneInfo

from sqlalchemy import Column, DateTime, ForeignKey, String, Table
from sqlalchemy.orm import relationship

from src.libs.sqlalchemy.base import mapper_registry
from src.users.models import Invitation

invitation_table = Table(
    "invitations",
    mapper_registry.metadata,
    Column("id", String(40), primary_key=True),
    Column(
        "created_at",
        DateTime(timezone=True),
        default=datetime.now(tz=ZoneInfo("UTC")),
        nullable=False,
    ),
    Column(
        "from_user_id",
        String(40),
        ForeignKey("users.id", ondelete="CASCADE", name="fk_invitations_user_id"),
        nullable=False,
    ),
    Column(
        "in_group_id",
        String(40),
        ForeignKey("groups.id", ondelete="CASCADE", name="fk_invitations_group_id"),
        nullable=False,
    ),
    Column(
        "with_roletype_id",
        String(40),
        ForeignKey(
            "roletypes.id", ondelete="CASCADE", name="fk_invitations_roletype_id"
        ),
        nullable=False,
    ),
    Column("to_user_email", String(250)),
    Column("hash", String(130)),
)


mapper_registry.map_imperatively(
    Invitation,
    invitation_table,
    properties={
        "from_user": relationship("User", back_populates="invitations"),
        "on_group": relationship("Group", back_populates="invitations"),
        "with_roletype": relationship("RoleType", back_populates="invitations"),
    },
)
