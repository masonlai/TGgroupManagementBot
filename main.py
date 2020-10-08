import telebot
import configparser
import requests
#from googleMap import ???

config = configparser.ConfigParser()
config.sections()
config.read('bot.conf')

bot = telebot.TeleBot(config['DEFAULTS']['bot_token'], parse_mode=None)

hki = config['DEFAULTS']['hki']
kw = config['DEFAULTS']['kw']
nt = config['DEFAULTS']['nt']
oi = config['DEFAULTS']['oi']

@bot.message_handler(commands=['pudding'])
def Cats(message):
    URL = 'https://api.thecatapi.com/v1/images/search?size=full'
    r = requests.get(url=URL)
    data = r.json()
    bot.send_photo(message.chat.id, data[0]['url'])


@bot.message_handler(commands=['foolishdog'])
def Dogs(message):
    URL = 'https://api.thedogapi.com/v1/images/search?size=full'
    r = requests.get(url=URL)
    data = r.json()
    bot.send_photo(message.chat.id, data[0]['url'])





