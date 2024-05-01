"""notifications

Revision ID: cd34a3bc55a9
Revises: eb892f48dbd8
Create Date: 2024-04-29 12:46:44.733110

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "cd34a3bc55a9"
down_revision = "eb892f48dbd8"
branch_labels = None
depends_on = None

messagetype_enum = sa.Enum("GROUP", "ROLE", "ROLETYPE", "TASK", "TAG", name="resources")


def upgrade() -> None:
    op.create_table(
        "subscriptions",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("tenant_id", sa.String(length=90), nullable=False),
        sa.Column("to", sa.String, nullable=False),
        sa.Column("cc", sa.String, nullable=False),
        sa.Column("bcc", sa.String, nullable=False),
        sa.Column("event_name", sa.String(length=150), nullable=False),
        sa.Column("event_type", messagetype_enum, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint(
            "event_name", "event_type", "to", name="subscriptions_events_to"
        ),
    )
    op.create_index(
        "subscriptions_events_to_index",
        "subscriptions",
        ["event_name", "event_type", "to"],
        unique=True,
    )
    op.create_table(
        "templates",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("name", sa.String(length=90), nullable=False),
        sa.Column("sender", sa.String(length=150), nullable=False),
        sa.Column("subject", sa.String(length=150), nullable=False),
        sa.Column("html", sa.String(length=150), nullable=False),
        sa.Column("text", sa.String(length=150), nullable=False),
        sa.Column("event_name", sa.String(length=150), nullable=False),
        sa.Column("event_type", messagetype_enum, nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("event_name", "event_type", name="templates_events"),
    )
    op.create_index(
        "templates_events_index", "templates", ["event_name", "event_type"], unique=True
    )
    op.create_table(
        "events",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("tenant_id", sa.String, nullable=False),
        sa.Column("name", sa.String, nullable=False),
        sa.Column("data", sa.types.JSON, nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_index("subscriptions_events_to_index", table_name="subscriptions")
    op.drop_table("subscriptions")
    op.drop_index("templates_events_index", table_name="templates")
    op.drop_table("templates")
    messagetype_enum.drop(op.get_bind(), checkfirst=False)
