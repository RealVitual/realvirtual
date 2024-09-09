import json
from django.contrib.auth import get_user_model
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import Message, Chat
# from src.apps.company.models import Conf
# from django.conf import settings

User = get_user_model()


class ChatConsumer(WebsocketConsumer):

    def fetch_messages(self, data):
        room = data['room']
        chat = Chat.objects.get(id=room)
        messages = chat.get_last_messages()
        content = {
            'command': 'messages',
            'messages': self.messages_to_json(messages)
        }
        self.send_message(content)

    def new_message(self, data):
        author = data['from']
        # conf, created = Conf.objects.get_or_create(pk=1)
        # words = conf.black_list_words.split(',')
        # emails = conf.black_list_emails.split(',')
        # if emails and author in emails:
        #     return None
        # if words:
        #     if any(ext in data['message'] for ext in words):
        #         return None
        if not data['message'].isspace():
            message = Message.objects.create(
                email=author, content=data['message'],
                names=data['names'], chat_id=data['room'])
            content = {
                'command': 'new_message',
                'message': self.message_to_json(message)
            }
            return self.send_chat_message(content)
        return None

    def messages_to_json(self, messages):
        result = []
        for message in messages:
            result.append(self.message_to_json(message))
        return result

    def message_to_json(self, message):
        # administrators = settings.NOTICE_ADMINS
        # admin = False
        # if message.email in administrators:
        #     admin = True
        return {
            'author': message.email,
            'content': message.content,
            'timestamp': str(message.timestamp),
            'names': message.names,
            # 'admin': admin
        }

    commands = {
        'fetch_messages': fetch_messages,
        'new_message': new_message
    }

    def connect(self):
        print('CONNECT!')
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat_%s' % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        data = json.loads(text_data)
        self.commands[data['command']](self, data)

    def send_chat_message(self, message):
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message
            }
        )

    def send_message(self, message):
        self.send(text_data=json.dumps(message))

    def chat_message(self, event):
        message = event['message']

        self.send(text_data=json.dumps(message))
