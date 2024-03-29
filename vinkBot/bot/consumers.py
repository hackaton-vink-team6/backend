import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer


class BotConsumer(WebsocketConsumer):
    """Перехватчик сообщений"""
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        get_response.delay(self.channel_name, text_data_json)

        async_to_sync(self.channel_layer.send)(
            self.channel_name,
            {
                "type": "chat_message",
                "text": {"msg": text_data_json["text"], "source": "user"},
            },
        )

    def chat_message(self, event):
        text = event["text"]
        self.send(text_data=json.dumps({"text": text}))
