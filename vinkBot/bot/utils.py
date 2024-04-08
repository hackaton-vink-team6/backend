from datetime import datetime

from bot.models import Message

def message_create(uuid, text, user_name):
    created_message = Message.objects.create(
                    uuid=uuid,
                    text=text,
                    user_name=user_name,
                    chat_id=chat_id)

    return created_message

