from django.db import models


class Message(models.Model):
    """Модель сообщения"""
    uuid = models.UUIDField(editable=False)
    text = models.TextField(verbose_name='Текст сообщения')
    pub_date = models.DateTimeField(auto_now_add=True, verbose_name='Время получения')
    user_name = models.TextField(verbose_name='Отправитель')
    chat_id = models.PositiveIntegerField()
