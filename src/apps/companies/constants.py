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
    CONFIRMED_REGISTER = 'Registro usuario confirmado'
    TO_CONFIRM_USER = 'Usuario por confirmar'
    PASSWORD = 'Recuperar/Reestablecer contraseña'
    SCHEDULE = 'Evento / Horario Agendado'
    WORKSHOP = 'Taller Agendado'
    WORKSHOP_WAITING = 'Taller en lista de espera Agendado'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]


class FontType(Enum):
    CSS_DMSANS = 'css-DMSans'
    CSS_INTERTIGHT = 'css-Intertight'

    @classmethod
    def choices(cls):
        return [(choice.name, choice.value) for choice in cls]
