from enum import Enum


class EncryptionType(Enum):
    SHA256 = 'Sha256 encryption algorithm'
    SHA512 = 'Sha512 encryption algorithm'
    MD5 = 'MD5  encryption algorithm'


class RequestType(Enum):
    Post = ('post', 'Post')
    Get = ('get', 'Get')
    Put = ('put', 'Put')
    Ntf = ('notification', 'Notification')
    Invoke = ('invoke', 'Invoke')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]

    @classmethod
    def choices(cls):
        return [choice.value for choice in cls]


class OutboundDataType(Enum):
    JSON = ('json', 'JSON')
    XML = ('xml', 'XML')

    @classmethod
    def get_value(cls, member):
        return cls[member].value[0]

    @classmethod
    def choices(cls):
        return [choice.value for choice in cls]
