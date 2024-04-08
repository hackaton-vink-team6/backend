import os

from django.conf import settings
from django.core.mail import send_mail
from api.models import Answer, Profile, Question
from bot.yandex_gpt.main import start
from django.core.management.base import BaseCommand
from telegram import Bot, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)
from telegram.utils.request import Request

TOKEN = os.getenv('TELEGRAM_TOKEN')
PROXY_URL = os.getenv('')


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
    text_question = update.message.text

    p, _ = Profile.objects.get_or_create(
        chat_id=chat_id,
        defaults={
            'name': update.message.from_user.username,
        }
    )
    Question(
        profile=p,
        text_question=text_question,
    ).save()

    if text_question=='Прошу человека':
        answer = None
        send_mail('vink', f'{chat_id} просит помощи.',
            settings.EMAIL_HOST_USER,  
            [settings.EMAIL_HOST_USER],
        ) 
    else:
        answer = start(text_question)

    if answer:
        Answer(
            profile=p,
            text_question=text_question,
            text_answer=answer
        ).save()

        reply_text = f'{answer}'
        update.message.reply_text(text=reply_text)

    else:
        update.message.reply_text(
            'Подождите, через несколько минут подключится другой специалист')


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
            connect_timeout=25.5,
            read_timeout=25.0,
        )
        bot = Bot(
            request=request,
            token=TOKEN,
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