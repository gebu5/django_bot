# Generated by Django 4.0.4 on 2022-04-25 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0007_telegrambots'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TelegramBots',
            new_name='TelegramBot',
        ),
    ]
