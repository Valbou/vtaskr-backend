from enum import Enum, IntFlag


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


# TODO: Resources = Enum("Resources", {"GROUP": "group", "ROLE": "role"})


class Permissions(IntFlag):
    READ = 1
    UPDATE = 2
    CREATE = 4
    DELETE = 8
    EXECUTE = 16
    SUSCRIBE = 32
