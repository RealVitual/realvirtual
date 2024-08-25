from enum import Enum


class AccessType(Enum):
    IN_PERSON = 'IN PERSON'
    VIRTUAL = 'VIRTUAL'
    HYBRID = 'HYBRID'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class EmailType(Enum):
    REGISTER = 'Registro completado'
    PASSWORD = 'Recuperar/Reestablecer contraseña'
    SCHEDULE = 'Confirmación de agenda'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
