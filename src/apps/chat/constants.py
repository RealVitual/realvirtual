from enum import Enum


class ChatType(Enum):
    EVENT = 'Para evento en vivo'
    USERS = 'Para usuarios solamente'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
