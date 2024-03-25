from django.db import models


class Message(models.Model):
    answer = models.TextField(verbose_name='Текст ответа')
    question = models.TextField(verbose_name='Текст вопроса')
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время получения',
    )
    is_liked = models.BooleanField(
        verbose_name="Понравился ли ответ",
        default=True
    )

    def __str__(self):
        return f'Ответ {self.answer[15:]} на вопрос {self.question[15:]}'

    class Meta:
        verbose_name = 'Сообщение от бота'
        verbose_name_plural = 'Сообщения от бота'
