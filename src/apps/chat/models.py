from django.db import models
from src.apps.events.models import Event
from .constants import ChatType
from src.contrib.db.models import BaseModel


class Chat(BaseModel):
    event = models.ForeignKey(
        Event, related_name="chats", on_delete=models.CASCADE,
        null=True
    )
    client = models.CharField(
        'Cliente', max_length=255, blank=True
    )
    code = models.CharField(
        'Codigo', max_length=255
    )
    name = models.CharField(
        'Nombre', max_length=255, blank=True
    )
    chat_type = models.CharField(
        'Tipo de uso', max_length=30, choices=ChatType.choices(),
        default=ChatType.EVENT)
    public = models.BooleanField('Es publico', default=False)

    def __str__(self):
        return self.name

    def get_last_messages(self):
        return self.chat_messages.exclude(content="").order_by(
            '-timestamp')[:50:-1]


class Message(BaseModel):
    chat = models.ForeignKey(
        Chat, related_name="chat_messages", on_delete=models.CASCADE
    )
    email = models.EmailField(
        'Email'
    )
    content = models.TextField()
    image = models.ImageField(
        'Imagen', upload_to='chat_images/', null=True, blank=True)
    names = models.CharField('Nombre', max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email
