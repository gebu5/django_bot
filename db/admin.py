from django.contrib import admin
from .models import Task, TelegramBot
from django_bot.forms import TaskForm, TimeForm


@admin.register(Task)
class MyModelAdmin(admin.ModelAdmin):
    list_display = ['country', 'time']
    #formfield_overrides = {
    #    Task.time: {'widget': TimeForm},
    #}

admin.site.register(TelegramBot)
