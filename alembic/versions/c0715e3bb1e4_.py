"""empty message

Revision ID: c0715e3bb1e4
Revises: a56f90b2adf6
Create Date: 2024-11-15 06:32:57.467812

"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "c0715e3bb1e4"
down_revision = "a56f90b2adf6"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("contacts_email_key", "contacts", type_="unique")
    op.drop_constraint("contacts_phone_number_key", "contacts", type_="unique")
    op.drop_constraint("contacts_telegram_key", "contacts", type_="unique")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint("contacts_telegram_key", "contacts", ["telegram"])
    op.create_unique_constraint(
        "contacts_phone_number_key", "contacts", ["phone_number"]
    )
    op.create_unique_constraint("contacts_email_key", "contacts", ["email"])
    # ### end Alembic commands ###