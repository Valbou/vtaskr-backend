from enum import IntFlag


class Permissions(IntFlag):
    READ = 1
    UPDATE = 2
    CREATE = 4
    DELETE = 8
    EXECUTE = 16
    SUSCRIBE = 32
