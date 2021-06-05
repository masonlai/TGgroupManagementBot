import telebot
import configparser
import requests
import sqlite3
import mplfinance as mpf
import yfinance as yf
import dbutil
import time
import threading
import os

config = configparser.ConfigParser()
config.sections()
config.read('bot_conf.cfg', encoding="utf-8-sig")
bot = telebot.TeleBot(os.getenv('TOKEN'), parse_mode=None)
botSentMsg = []


@bot.message_handler(commands=['pudding'])
def Cats(message):
    bot.delete_message(message.chat.id, message.message_id)
    URL = 'https://api.thecatapi.com/v1/images/search?size=full'
    r = requests.get(url=URL)
    data = r.json()
    botSentMsg.append(bot.send_photo(message.chat.id, data[0]['url']))


@bot.message_handler(commands=['foolishdog'])
def Dogs(message):
    bot.delete_message(message.chat.id, message.message_id)
    URL = 'https://api.thedogapi.com/v1/images/search?size=full'
    r = requests.get(url=URL)
    data = r.json()
    botSentMsg.append(bot.send_photo(message.chat.id, data[0]['url']))


@bot.message_handler(commands=['lovecfu'])
def Stock(message):
    bot.delete_message(message.chat.id, message.message_id)
    try:
        msft = yf.Ticker(message.text.split(' ')[1])
        ohlc = msft.history(period="1mo")
        ohlc.index.name = 'Date'
        ohlc.shape
        ohlc.head(3)
        ohlc.tail(3)
        mpf.plot(ohlc, type='candle', savefig='chart.png', style='charles')
        photo = open('chart.png', 'rb')
        botSentMsg.append(bot.send_message(message.chat.id, "資料來源Yahoo Finance唔準唔負責", parse_mode=None))
        botSentMsg.append(bot.send_photo(message.chat.id, photo))

    except:
        botSentMsg.append(
            bot.send_message(message.chat.id, '傻仔{0}, 淨係睇到美股. 一係你比錢我買API'.format(message.from_user.username),
                             parse_mode=None))


@bot.message_handler(commands=['get'])
def get(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    print(msg)



@bot.message_handler(commands=['approve'])
def approve(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    if msg.from_user.id == 937935148:
        try:
            if msg.reply_to_message != None:
                dbutil.updateApprover(msg.reply_to_message.from_user.id)
        except:
            pass
    else:
        botSentMsg.append(bot.send_message(msg.chat.id, '含撚啦,你邊個啊?',
                                           parse_mode=None))


@bot.message_handler(commands=['reg'])
def approve(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    approverList = dbutil.getApprovers()
    if msg.from_user.id in approverList:
        if msg.reply_to_message != None:
            dbutil.updatelist(msg.reply_to_message.from_user.id)
    else:
        botSentMsg.append(bot.send_message(msg.chat.id, '含撚啦,你邊個啊?',
                                           parse_mode=None))


@bot.message_handler(commands=['dereg'])
def approve(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    approverList = dbutil.getApprovers()
    if msg.from_user.id in approverList:
        if msg.reply_to_message != None:
            dbutil.deleteCallList(msg.reply_to_message.from_user.id)
    else:
        botSentMsg.append(bot.send_message(msg.chat.id, '含撚啦,你邊個啊?',
                                           parse_mode=None))


@bot.message_handler(commands=['refuse'])
def refuse(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    if msg.from_user.id == 937935148:
        if msg.reply_to_message != None:
            dbutil.deleteApproveList(msg.reply_to_message.from_user.id)
    else:
        botSentMsg.append(bot.send_message(msg.chat.id, '含撚啦,你邊個啊?',
                                           parse_mode=None))


@bot.message_handler(commands=['callup'])
def callup(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    approverList = dbutil.getApprovers()
    if msg.from_user.id in approverList:
        callupList = dbutil.getCallList()
        string = "*嘉琳軍最後召集*"
        for index, i in enumerate(callupList):
            member = "\n[嘉琳{}](tg://user?id={})".format(index + 1, i)
            string += member
        botSentMsg.append(bot.send_message(msg.chat.id, string, parse_mode="MarkdownV2"))
    else:
        botSentMsg.append(bot.send_message(msg.chat.id, '含撚啦,你邊個啊?',
                                           parse_mode=None))

@bot.message_handler(commands=['clear'])
def callup(msg):
    bot.delete_message(msg.chat.id, msg.message_id)
    deleteMsg()

def cronJob():
    while (True):
        if len(botSentMsg)>0:
            time.sleep(5 * 60)
            deleteMsg()


def deleteMsg():
    for i in botSentMsg:
        bot.delete_message(i.chat.id, i.message_id)
    botSentMsg.clear()


added_thread = threading.Thread(target=cronJob, name='new_added_thread')
added_thread.start()

bot.polling(none_stop=True)
