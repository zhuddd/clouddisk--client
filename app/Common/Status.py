from enum import Enum


class Status(Enum):
    ERROR = -1
    NOT_STARTED = 0
    WAITING = 1
    DOWNLOADING = 2
    PAUSED = 3
    SUCCESS = 4
