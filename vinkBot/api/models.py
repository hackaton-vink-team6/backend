from django.db import models


class Profile(models.Model):
    name = models.TextField(verbose_name='Имя пользователя')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'


class Question(models.Model):
    profile = models.ForeignKey(
        Profile,
        verbose_name='Профиль',
        on_delete= models.CASCADE,
    )
    text_question = models.TextField(verbose_name='Текст вопроса', )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Время',
    )
    def __str__(self):
        return self.text_question


class Answer(Question):
    text_answer = models.TextField(
        verbose_name='Текст ответа',
        blank=True
    )

    def __str__(self):
        return self.text_answer

    class Meta:
        verbose_name = 'Сообщение от бота'
        verbose_name_plural = 'Сообщения от бота'
