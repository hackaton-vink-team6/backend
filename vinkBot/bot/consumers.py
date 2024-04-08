import json
import uuid
from datetime import datetime

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from bot.yandex_gpt.index import get_gpt_response
from bot.models import Message
from bot.utils import message_create


class BotConsumer(WebsocketConsumer):

    def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.uuid = self.scope['query_string'].decode('utf-8')
        if self.uuid:
            self.channel_layer(
                self.uuid,
                self.channel_name
            )
            messages = Message.objects.filter(id = self.uuid).order_by('-pub_date')

        else:
            self.new_uuid = str(uuid.uuid4())
            async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "send_uuid",
                "uuid": self.new_uuid,
            },
            )

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['text']
        if self.uuid:
            message_create(self.uuid, message, 'user', 'chat_message', self.chat_id)
        else:
            message_create(self.new_uuid, message, 'user', 'chat_message', self.chat_id)

        self.response_text = get_gpt_response(message)

        if self.uuid:
            message_create(self.uuid, self.response_text, 'bot', 'chat_message', self.chat_id)
        else:
            message_create(self.new_uuid, self.response_text, 'bot', 'chat_message', self.chat_id)


        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "chat_message",
                "text": message,
            },
            )

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "chat.message",
                "text": self.response_text,
            },
            )

    def chat_message(self, event):
        """Отправление сообщения в чат"""

        self.send(text_data=json.dumps({
            'chat_id': self.chat_id,
            'type': 'chat_message',
            'time': f'{datetime.now()}',
            'text': event['text']
        }, ensure_ascii=False))

    def send_uuid(self, event):
        """Отправление uuid клиенту"""

        self.send(text_data=json.dumps({
            'chat_id': self.chat_id,
            'type': 'uuid',
            'time': f'{datetime.now()}',
            'text': event['uuid']
        }))

