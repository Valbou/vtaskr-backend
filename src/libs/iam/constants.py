from enum import Enum, IntFlag, auto


class Resources(str, Enum):
    # Users
    GROUP = "group"
    ROLE = "role"
    ROLETYPE = "roletype"

    # Tasks
    TASK = "task"
    TAG = "tag"

    # Nofitications
    SUBSCRIPTION = "subscription"


class Permissions(IntFlag):
    READ = auto()
    ACHIEVE = auto()
    UPDATE = auto()
    CREATE = auto()
    DELETE = auto()
    SUSCRIBE = auto()
