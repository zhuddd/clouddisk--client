from enum import Enum


class Status(Enum):
    ERROR = -1
    NOT_STARTED = 0
    WAITING = 1
    RUNNING = 2
    PAUSED = 3
    SUCCESS = 4
