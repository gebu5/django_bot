import json
import threading

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import LoginForm, TaskForm
from db.models import Task
from bot import BotViza


apps = []

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


def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect('/login')

    context = {}
    tasks = {}
    for row in Task.objects.all():
        tasks[str(row)] = [
            row.id,
            row.accounts,
            row.is_running
        ]

    context['tasks'] = tasks

    if request.method == 'POST':
        form = TaskForm(request.POST)
        context['form'] = form

        if form.is_valid():
            new_task = Task(country=form.cleaned_data['country_'],
                            city=form.cleaned_data['city'],
                            date=form.cleaned_data['date'],
                            accounts=form.cleaned_data['accounts'])
            new_task.save()

            messages.success(request, 'Форма успешно отправлена')
            return HttpResponseRedirect('/')
        else:
            messages.error(request, 'Какие-то поля были заполнены неверно!')

    form = TaskForm()
    context['form'] = form

    return render(request, 'home/index.html', context=context)


def run_task(request, task_id):
    global apps
    apps = []
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
    accounts_list = []
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
    with open('info.json', 'w') as f:
        json.dump(file, f, indent=4, ensure_ascii=False)

    instance.save()
    app = BotViza()
    apps.append(app)
    threading.Thread(target=app.start_app, daemon=True).start()

    return HttpResponseRedirect('/')


def stop_task(request, task_id):
    global apps
    print(f'stop - {task_id}')
    instance = Task.objects.get(id=task_id)
    instance.is_running = False
    if apps:
        apps[0].end.put('stop')
    instance.save()

    return HttpResponseRedirect('/')


def delete_task(request, task_id):
    print(f'delete - {task_id}')
    instance = Task.objects.get(id=task_id)
    instance.delete()

    return HttpResponseRedirect('/')
