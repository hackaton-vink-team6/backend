# Generated by Django 4.0 on 2024-03-29 07:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.PositiveIntegerField()),
                ('name', models.TextField(verbose_name='Имя пользователя')),
            ],
            options={
                'verbose_name': 'Профиль',
                'verbose_name_plural': 'Профили',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text_question', models.TextField(verbose_name='Текст вопроса')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Время')),
                ('profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='api.profile', verbose_name='Профиль')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('question_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='api.question')),
                ('text_answer', models.TextField(blank=True, verbose_name='Текст ответа')),
            ],
            options={
                'verbose_name': 'Сообщение от бота',
                'verbose_name_plural': 'Сообщения от бота',
            },
            bases=('api.question',),
        ),
    ]
