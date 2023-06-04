"""initial structure

Revision ID: 89bc9a39daa4
Revises:
Create Date: 2023-06-04 18:59:35.012274

"""
import sqlalchemy as sa

from alembic import op
from vtaskr.users.models import RequestType

# revision identifiers, used by Alembic.
revision = "89bc9a39daa4"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column("first_name", sa.String(25)),
        sa.Column("last_name", sa.String(25)),
        sa.Column("email", sa.String(250), unique=True),
        sa.Column("hash_password", sa.String(256)),
        sa.Column("locale", sa.String(5)),
        sa.Column("timezone", sa.String(35)),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "last_login_at", sa.DateTime(timezone=True), nullable=True, default=None
        ),
    )

    op.create_table(
        "tokens",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column(
            "last_activity_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column("temp", sa.Boolean),
        sa.Column("temp_code", sa.String(12)),
        sa.Column("sha_token", sa.String(64), unique=True),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id")),
    )

    op.create_table(
        "requestschanges",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column("request_type", sa.Enum(RequestType)),
        sa.Column("email", sa.String),
        sa.Column("code", sa.String(12)),
        sa.Column("done", sa.Boolean),
    )

    op.create_table(
        "tasks",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id")),
        sa.Column("title", sa.String(150)),
        sa.Column("description", sa.String),
        sa.Column("emergency", sa.Boolean, default=False),
        sa.Column("important", sa.Boolean, default=False),
        sa.Column(
            "scheduled_at", sa.DateTime(timezone=True), nullable=True, default=None
        ),
        sa.Column("duration", sa.Interval, nullable=True, default=None),
        sa.Column("done", sa.DateTime(timezone=True), nullable=True, default=None),
    )

    op.create_table(
        "tags",
        sa.Column("id", sa.String, primary_key=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.current_timestamp(),
        ),
        sa.Column("user_id", sa.String, sa.ForeignKey("users.id")),
        sa.Column("title", sa.String(50)),
        sa.Column("color", sa.String(20)),
    )

    op.create_table(
        "taskstags",
        sa.Column("tag_id", sa.String, sa.ForeignKey("tags.id"), primary_key=True),
        sa.Column("task_id", sa.String, sa.ForeignKey("tasks.id"), primary_key=True),
    )


def downgrade() -> None:
    op.drop_table("taskstags")
    op.drop_table("tags")
    op.drop_table("tasks")
    op.drop_table("requestschanges")
    op.drop_table("tokens")
    op.drop_table("users")
    conn = op.get_bind()
    conn.execute(sa.text("DROP TYPE requesttype;"))
