from enum import Enum, IntFlag, auto


class Resources(str, Enum):
    # Users
    GROUP = "group"
    ROLETYPE = "roletype"

    # Tasks
    TASK = "task"
    TAG = "tag"


class Permissions(IntFlag):
    READ = auto()
    ACHIEVE = auto()
    UPDATE = auto()
    CREATE = auto()
    DELETE = auto()
