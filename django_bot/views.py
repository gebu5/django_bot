import json
import threading

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm, TaskForm, TelegramAttachForm
from db.models import Task, TelegramBot
from bot import BotViza, add_task_message, end_message, check_telegram_bot
from directory_info import dict_countries, dict_cities


def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')

    context = {}

    if request.method == 'POST':
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/')
                else:
                    return HttpResponse('Disabled account')
            else:
                context['login_message'] = 'Неверный логин или пароль!'
                return render(request, 'home/login.html', context)
    else:
        form = LoginForm()
        context['form'] = form
    return render(request, 'home/login.html', context)


def user_logout(request):
    logout(request)

    return HttpResponseRedirect('/login')


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    context = {}
    telegram_attach_form = TelegramAttachForm()
    context['telegram_attach_form'] = telegram_attach_form

    tasks_to_show = {}
    time_test = Task.objects.all().order_by('time')
    for tt in time_test:
        print(tt.time.minute)
    for row in Task.objects.all():
        if row.account_id == request.user.id:
            tasks_to_show[str(row)] = [
                row.id,
                row.accounts,
                row.is_running
            ]

    context['tasks'] = tasks_to_show

    if request.method == 'POST':
        form = TaskForm(request.POST)
        context['form'] = form

        if form.is_valid():
            if not TelegramBot.objects.filter(account_id=request.user.id):
                messages.error(request, 'Необходимо привязать телеграмм бота!')
                form = TaskForm()
                context['form'] = form
                return render(request, 'home/index.html', context=context)

            new_task = Task(country=form.cleaned_data['country_'],
                            city=form.cleaned_data['city'],
                            date=form.cleaned_data['date'],
                            accounts=form.cleaned_data['accounts'],
                            account_id=request.user.id)
            new_task.save()

            messages.success(request, 'Форма успешно отправлена')
            country = dict_countries[form.cleaned_data['country_']]
            city = dict_cities[form.cleaned_data['city']]
            add_task_message(country, city, request.user.id)
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Какие-то поля были заполнены неверно!')

    form = TaskForm()
    context['form'] = form

    return render(request, 'home/index.html', context=context)


def attach_telegram(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    if request.method == 'POST':
        telegram_attach_form = TelegramAttachForm(request.POST)

        if telegram_attach_form.is_valid():
            bot_api = telegram_attach_form.cleaned_data['api_key']
            chat_url = telegram_attach_form.cleaned_data['chat_url']
            channel_name = f'@{chat_url.split("/")[-1]}'
            result = check_telegram_bot(bot_api, channel_name)
            if 'success' in result:
                messages.success(request, 'Телеграмм бот успешно привязан', extra_tags='telegram')
                for row in TelegramBot.objects.filter(account_id=request.user.id):
                    row.delete()
                new_bot = TelegramBot(api_key=bot_api, channel_name=channel_name, account_id=request.user.id)
                new_bot.save()
            else:
                messages.error(request, result, extra_tags='telegram')
        else:
            messages.error(request, 'Ошибка, перепроверьте данные!', extra_tags='telegram')

    return HttpResponseRedirect('/')


def run_task(request, task_id):
    print(f'run - {task_id}')
    instance = Task.objects.get(id=task_id)
    instance.is_running = True
    accounts = instance.accounts.split('\n')
    country = instance.country
    city = instance.city
    date = instance.date
    thread_info = {}
    date = date.split('-')
    month = date[1] if '0' not in date[1] else date[1][1]
    date = f'{month}/1/{date[0]}'
    thread_info['country'] = country
    thread_info['city'] = city
    thread_info['date'] = date
    thread_info['task_id'] = task_id
    accounts_list = []
    print('check  --  ' + str(len(accounts)))
    for account in accounts:
        account_dict = {}
        account_dict['barcode'] = account.split(';')[0]
        account_dict['surname'] = account.split(';')[1]
        account_dict['givenname'] = account.split(';')[2]
        account_dict['passport'] = account.split(';')[3]
        account_dict['email'] = account.split(';')[4]
        account_dict['phone'] = account.split(';')[5]
        accounts_list.append(account_dict)
    file = {'thread_info': thread_info, 'accounts': accounts_list}
    with open('info.json', 'w', encoding='UTF-8') as f:
        json.dump(file, f, indent=4, ensure_ascii=False)

    instance.save()
    app = BotViza(request.user.id)
    app.start_message(dict_countries[country], dict_cities[city])
    threading.Thread(target=app.start_app, daemon=True).start()
    return HttpResponseRedirect('/')


def stop_task(request, task_id):
    print(f'stop - {task_id}')
    instance = Task.objects.get(id=task_id)
    instance.is_running = False
    instance.save()

    return HttpResponseRedirect('/')


def delete_task(request, task_id):
    print(f'delete - {task_id}')
    instance = Task.objects.get(id=task_id)
    end_message(dict_countries[instance.country], dict_cities[instance.city], request.user.id)
    instance.delete()

    return HttpResponseRedirect('/')
