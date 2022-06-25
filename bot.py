import json
import telebot
import threading
import time

from core import Submiter
from utils import lprint
from queue import Queue
from db.models import Task, TelegramBot
from pyvirtualdisplay import Display
from directory_info import dict_countries, dict_cities


class BotViza():
    def __init__(self, account_id):
        instance = TelegramBot.objects.get(account_id=account_id)
        self.bot = telebot.TeleBot(instance.api_key)
        self.channel_name = instance.channel_name
        self.q = Queue()
        with open('config.json') as f:
            self.config = json.load(f)
        with open('info.json') as f:
            self.info = json.load(f)
            self.accounts = self.info['accounts']
            self.thread_info = self.info['thread_info']
        for account in self.accounts:
            self.q.put(account)
        self.end = Queue()

    def start_bot(self):
        numbot = 0
        while True:
            if self.end.qsize():
                print('death')
                return
            if not self.q.qsize():
                time.sleep(5)
                continue
            account = self.q.get()
            while True:
                if self.end.qsize():
                    print('death')
                    return
                numbot += 1
                try:
                    submit = Submiter(self.bot, numbot, account['barcode'], account['surname'], account['givenname'],
                                  account['passport'], account['email'], account['phone'], self.config['delay'],
                                  self.thread_info['country'], self.thread_info['city'], self.thread_info['date'], self.channel_name)
                except:
                    lprint('Error while create selenium')
                    continue
                try:
                    result = submit.body(self.end)
                    break
                except Exception as error:
                    lprint('Error while working thread' + str(error))
                    submit.driver.quit()
                    continue

            if 'end_task' in result:
                submit.driver.quit()
                continue
            if result == 'Bad acc':
                submit.driver.quit()
                self.q.put(account)
                continue

            self.accounts.remove(account)
            self.info['accounts'] = self.accounts
            with open('info.json', 'w') as f:
                json.dump(self.info, f, indent=4)
            print('Account succecfully registred!')
            submit.driver.quit()

    def start_app(self):
        #display = Display(visible=False, size=(1100, 900))
        #display.start()
        threading.Thread(target=self.check_stop, daemon=True).start()
        threads = []
        numb_threads = len(self.accounts)//10
        if not numb_threads:
            numb_threads = 1
        if numb_threads > 10:
            numb_threads = 10
        print('threads' + str(numb_threads))
        for i in range(numb_threads):
            thread = threading.Thread(target=self.start_bot, daemon=True)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        print('end')
        #display.stop()
        return

    def start_message(self, country, city):
        self.bot.send_message(self.channel_name, f'Запущен бот - Страна : {country}|'
                                            f'Город : {city}')

    def stop_message(self, country, city):
        self.bot.send_message(self.channel_name, f'Остановлен бот - Страна : {country}|'
                                            f'Город : {city}')

    def check_stop(self):
        while True:
            try:
                instance = Task.objects.get(id=self.thread_info['task_id'])
            except Task.DoesNotExist:
                self.end.put('stop')
                return
            if not instance.is_running:
                self.end.put('stop')
                self.stop_message(dict_countries[instance.country], dict_cities[instance.city])
                return
            time.sleep(1)


def end_message(country, city, user_id):
    instance = TelegramBot.objects.get(account_id=user_id)
    api_key = instance.api_key
    channel_name = instance.channel_name
    bot = telebot.TeleBot(api_key)
    bot.send_message(channel_name, f'Удален бот - Страна : {country}|'
                                   f'Город : {city}')


def add_task_message(country, city, user_id):
    instance = TelegramBot.objects.get(account_id=user_id)
    api_key = instance.api_key
    channel_name = instance.channel_name
    bot = telebot.TeleBot(api_key)
    bot.send_message(channel_name, f'Добавлен бот - Страна : {country}|'
                                   f'Город : {city}')


def check_telegram_bot(api_key, channel_name):
    bot = telebot.TeleBot(api_key)
    try:
        bot.send_message(channel_name, 'Телеграм бот успешно привязан к вашему аккаунту!')
        message = 'success'
    except Exception as error:
        if 'A request to the Telegram API was unsuccessful. Error code: 404. Description: Not Found' in str(error):
            message = 'Неправильный API ключ бота'
        elif 'chat not found' in str(error):
            message = 'Телеграмм группа не найдена'
        elif 'bot is not a member of the channel chat' in str(error):
            message = 'Бот не участник группы или не имеет доступа на публикацию!'
        else:
            message = 'Возникла ошибка, перепроверьте данные и попробуйте позже'
    return message
