import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from django.contrib.sessions.backends.db import SessionStore


class BotConsumer(WebsocketConsumer):
    """Перехватчик сообщений"""
    def connect(self):
        session = SessionStore()
        session.create()
        self.session_id = session.session_key

        self.chat_history = []

        self.accept()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        if message:
            self.chat_history += f"User: {message}\n"

            response_text = get_gpt_response.delay(message)

            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    "type": "chat.message",
                    "text": {"msg": response_text, "source": "bot"},
                },
                )

            async_to_sync(self.channel_layer.send)(
                self.channel_name,
                {
                    "type": "chat_message",
                    "text": {"msg": text_data_json["text"], "source": "user"},
                },
                )

    def disconnect(self, close_code):
        SessionStore(session_key=self.session_id).delete()

    def chat_message(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({"text": text}))
