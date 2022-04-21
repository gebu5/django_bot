import json
import telebot
import threading

from core import Submiter
from utils import lprint
from queue import Queue
from pyvirtualdisplay import Display


class BotViza():
    def __init__(self):
        self.terminate = False
        self.q = Queue()
        with open('config.json') as f:
            self.config = json.load(f)
        if self.config['test_mode']:
            self.bot = telebot.TeleBot('5216298767:AAFYJ1_TB2yf7W_cAF-fPoCuQQvTxOMjWSA')
        else:
            self.bot = telebot.TeleBot('5072504401:AAFTrek5kZM8cdQFEdCoW8SWa8S7uRAbM9Q')
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
            account = self.q.get()
            if self.end.qsize():
                return
            while True:
                numbot += 1
                submit = Submiter(self.bot, numbot, account['barcode'], account['surname'], account['givenname'],
                                  account['passport'], account['email'], account['phone'], self.config['delay'],
                                  self.thread_info['country'],self.thread_info['city'], self.thread_info['date'], self.config['test_mode'])
                try:
                    result = submit.body(self.end)
                    break
                except Exception as error:
                    lprint('Ошибка во время прохода' + str(error))
                    submit.driver.quit()
                    continue

            if not result:
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
            print('Аккаунт успешно зарегистрирован!')
            submit.driver.quit()

    def start_app(self):
        display = Display(visible=False, size=(1100, 900))
        display.start()
        threads = []
        for i in range(self.config['threads']):
            thread = threading.Thread(target=self.start_bot, daemon=True)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        print('end')
        display.stop()
        return


