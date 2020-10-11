import telebot
import configparser
import requests

import mplfinance as mpf
import yfinance as yf

# from googleMap import ???

# read the bot_conf.cfg
config = configparser.ConfigParser()
config.sections()
config.read('bot_conf.cfg', encoding="utf-8-sig")

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


@bot.message_handler(commands=['yellowshop'])
def YellowShop(message):
    area = '旺角'
    type = '日式'
    list_type = requests.get(root_api + 'area_type', params={"area": area})
    list = requests.get(config['DEFAULTS']['list_api'] + 'shop', params={"area": area, "type": type})
    bot.send_message(message.chat.id, list, parse_mode=None)


# @bot.message_handler(commands=['lovecfu'])
# def Stock(message):
#     try:
#         msft = yf.Ticker(message.text.split(' ')[1])
#         ohlc = msft.history(period="1mo")
#         ohlc.index.name = 'Date'
#         ohlc.shape
#         ohlc.head(3)
#         ohlc.tail(3)
#         mpf.plot(ohlc, type='candle',savefig='chart.png',style='charles')
#         photo = open('chart.png', 'rb')
#         bot.send_message(message.chat.id, "資料來源Yahoo Finance唔準唔負責", parse_mode=None)
#         bot.send_photo(message.chat.id, photo)
#
#     except TypeError as e:
#         bot.send_message(message.chat.id, '傻仔{0}, 淨係睇到美股. 一係你比錢我買API'.format(message.from_user.username), parse_mode=None)



bot.polling(none_stop=True)
