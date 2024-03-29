import os

from typing import Any
from django.core.management.base import BaseCommand

from telegram import Bot, Update
from telegram.ext import Updater, Filters, CallbackContext, MessageHandler, CommandHandler
from telegram.utils.request import Request


from api.models import Question, Profile

TOKEN='6917372678:AAFC89KdLfU0mj9E-M7hlhRtrgXYPMpaGuA'
PROXY_URL=os.getenv('')

def log_errors(f):

    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            error_message = f'Ошибка: {e}'
            print(error_message)
            raise e
    
    return inner


@log_errors
def do_echo(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text

    p, _ = Profile.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    Question(
        profile=p,
        text_question=text,
    ).save()

    reply_text = f'{chat_id} and {text}'
    update.message.reply_text(text=reply_text)


@log_errors
def do_count(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id

    p, _ = Profile.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    count = Question.objects.filter(profile=p).count()

    update.message.reply_text(text=f'У вас {count} сообщений')


class Command(BaseCommand):
    help = 'Бот'

    def handle(self, *args, **options):
        request = Request(
            connect_timeout=5.5,
            read_timeout=5.0,
        )
        bot = Bot(
            request=request,
            token=TOKEN,
            ########base_url=PROXY_URL,
        )
        print(bot.get_me())

        updater = Updater(
            bot=bot,
            use_context=True,
        )

        message_handler = MessageHandler(Filters.text, do_echo)
        updater.dispatcher.add_handler(message_handler)

        count_handler = CommandHandler('count', do_count)
        updater.dispatcher.add_handler(count_handler)

        updater.start_polling()
        updater.idle()