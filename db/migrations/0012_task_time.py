# Generated by Django 4.0.4 on 2022-06-21 13:46

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('db', '0011_remove_task_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='time',
            field=models.TimeField(default=datetime.datetime(2022, 6, 21, 13, 46, 46, 726492, tzinfo=utc), verbose_name='Time'),
        ),
    ]