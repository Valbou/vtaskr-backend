# Users Module
# Tasks Module
from vtaskr.tasks.persistence.sqlalchemy.tables import (
    tag_table,
    tasks_table,
    tasktag_table,
)
from vtaskr.users.persistence.sqlalchemy.tables import (
    request_change_table,
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
]
