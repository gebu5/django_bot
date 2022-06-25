from django.db import models
from django.utils import timezone
from django_bot.forms import TimeForm


class Task(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    accounts = models.CharField(max_length=5000)
    account_id = models.PositiveIntegerField(default=0)
    is_running = models.BooleanField(default=False)
    time = models.TimeField(default=timezone.now(), verbose_name='Time', auto_now_add=False)


    def __str__(self):
        self_info = f'{self.id} | {self.country} | {self.city} | {self.date}'

        return self_info


class TelegramBot(models.Model):
    api_key = models.CharField(max_length=200)
    channel_name = models.CharField(max_length=200)
    account_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        self_info = f'{self.api_key} | {self.channel_name} | {self.account_id}'

        return self_info
