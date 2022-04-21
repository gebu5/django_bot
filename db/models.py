from django.db import models


class Task(models.Model):
    country = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    date = models.CharField(max_length=200)
    accounts = models.CharField(max_length=5000)
    is_running = models.BooleanField(default=False)

    def __str__(self):
        self_info = f'{self.country} | {self.city} | {self.date}'

        return self_info

