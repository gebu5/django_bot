import telebot


def send_file_to_channel(file):
    bot = telebot.TeleBot('5072504401:AAFTrek5kZM8cdQFEdCoW8SWa8S7uRAbM9Q')

    CHANNEL_NAME = '@bottestvisa'
    bot.send_document(CHANNEL_NAME, document=open(file, 'rb'))









