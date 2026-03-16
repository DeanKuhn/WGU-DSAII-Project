from enum import Enum

class Status(Enum):
    DELAYED = 1
    AT_HUB = 2
    EN_ROUTE = 3
    DELIVERED = 4