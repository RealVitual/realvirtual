from enum import Enum


class AccessType(Enum):
    IN_PERSON = 'IN PERSON'
    VIRTUAL = 'VIRTUAL'
    HYBRID = 'HYBRID'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
