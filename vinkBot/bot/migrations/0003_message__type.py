# Generated by Django 4.2.1 on 2024-04-04 16:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("bot", "0002_remove_message_text_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="message",
            name="_type",
            field=models.TextField(default=1, verbose_name="Тип сообщения"),
            preserve_default=False,
        ),
    ]