from enum import Enum


class ConnectionType(Enum):
    END2START = "end2start"
    START2END = "start2end"
    START2START = "start2start"
    END2END = "end2end"
    DISCONNECTED = "disconnected"