# Users Module
# Tasks Module
from src.tasks.persistence.sqlalchemy.tables import (
    tag_table,
    tasks_table,
    tasktag_table,
)
from src.users.persistence.sqlalchemy.tables import (
    group_table,
    request_change_table,
    right_table,
    role_table,
    roletype_table,
    token_table,
    user_table,
)

INIT = True
LIST_TABLES = [
    user_table,
    token_table,
    request_change_table,
    tasks_table,
    tag_table,
    tasktag_table,
    group_table,
    roletype_table,
    right_table,
    role_table,
]
