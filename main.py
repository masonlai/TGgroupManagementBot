import telebot
import configparser
import requests
import mplfinance as mpf
import yfinance as yf
import dbutil
import time
import threading
import os
import logging

config = configparser.ConfigParser()
config.sections()
config.read('bot_conf.cfg', encoding="utf-8-sig")
bot = telebot.TeleBot(os.getenv('TOKEN'), parse_mode=None)
botSentMsg = []
logging.basicConfig(filename='tgBotLog.log',
                            filemode='a',level=logging.INFO, datefmt='%Y-%m-%d %H:%M:%S',  format='%(asctime)s %(levelname)-8s %(message)s')


@bot.message_handler(commands=['pudding'])
def Cats(message):
    logging.info("User:%s ,Using function: %s" % (message.from_user.username, "cat"))
    try:
        try:
            bot.delete_message(message.chat.id, message.message_id)
        except:
            logging.info("no right to delete msg, Group:%s".format(message.chat.title))
        URL = 'https://api.thecatapi.com/v1/images/search?size=full'
        r = requests.get(url=URL)
        data = r.json()
        botSentMsg.append(bot.send_photo(message.chat.id, data[0]['url']))
    except Exception as e:
        logging.error("unexpected error: %s".format(e))


@bot.message_handler(commands=['foolishdog'])
def Dogs(message):
    logging.info("User:%s ,Using function: %s" % (message.from_user.username, "dogs"))
    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(message.chat.title))
    URL = 'https://api.thedogapi.com/v1/images/search?size=full'
    r = requests.get(url=URL)
    data = r.json()
    botSentMsg.append(bot.send_photo(message.chat.id, data[0]['url']))


@bot.message_handler(commands=['lovecfu'])
def Stock(message):
    logging.info("User:%s ,Using function: %s" % (message.from_user.username, "lovecfu"))

    try:
        bot.delete_message(message.chat.id, message.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(message.chat.title))
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
    logging.info("User:%s ,Using function: %s" % (msg.from_user.username, "get"))
    try:
        bot.delete_message(msg.chat.id, msg.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(msg.chat.title))
    print(msg.reply_to_message.from_user.id)


@bot.message_handler(commands=['approve'])
def approve(msg):
    logging.info("User:%s ,Using function: %s" % (msg.from_user.username, "approve"))
    try:
        bot.delete_message(msg.chat.id, msg.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(msg.chat.title))
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
    logging.info("User:%s ,Using function: %s" % (msg.from_user.username, "approve"))
    try:
        bot.delete_message(msg.chat.id, msg.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(msg.chat.title))
    approverList = dbutil.getApprovers()
    if msg.from_user.id in approverList:
        if msg.reply_to_message != None:
            dbutil.updatelist(msg.reply_to_message.from_user.id)
    else:
        botSentMsg.append(bot.send_message(msg.chat.id, '含撚啦,你邊個啊?',
                                           parse_mode=None))


@bot.message_handler(commands=['dereg'])
def approve(msg):
    logging.info("User:%s ,Using function: %s" % (msg.from_user.username, "dereg"))
    try:
        bot.delete_message(msg.chat.id, msg.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(msg.chat.title))
    approverList = dbutil.getApprovers()
    if msg.from_user.id in approverList:
        if msg.reply_to_message != None:
            dbutil.deleteCallList(msg.reply_to_message.from_user.id)
    else:
        botSentMsg.append(bot.send_message(msg.chat.id, '含撚啦,你邊個啊?',
                                           parse_mode=None))


@bot.message_handler(commands=['refuse'])
def refuse(msg):
    logging.info("User:%s ,Using function: %s" % (msg.from_user.username, "refuse"))
    try:
        bot.delete_message(msg.chat.id, msg.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(msg.chat.title))
    if msg.from_user.id == 937935148:
        if msg.reply_to_message != None:
            dbutil.deleteApproveList(msg.reply_to_message.from_user.id)
    else:
        botSentMsg.append(bot.send_message(msg.chat.id, '含撚啦,你邊個啊?',
                                           parse_mode=None))


@bot.message_handler(commands=['callup'])
def callup(msg):
    logging.info("User:%s ,Using function: %s" % (msg.from_user.username, "callup"))
    try:
        bot.delete_message(msg.chat.id, msg.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(msg.chat.title))
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
def clear(msg):
    logging.info("User:%s ,Using function: %s" % (msg.from_user.username, "clear"))
    try:
        bot.delete_message(msg.chat.id, msg.message_id)
    except:
        logging.info("no right to delete msg, Group:%s".format(msg.chat.title))
    deleteMsg()


@bot.message_handler(func=lambda m: True)
def echo_all(message):
    if message.from_user.id == 876967414:
        bot.delete_message(message.chat.id, message.message_id)

	# bot.reply_to(message, message.text)

# def cronJob():
#     while (True):
#         if len(botSentMsg) > 0:
#             time.sleep(5 * 60)
#             deleteMsg()


def deleteMsg():
    for i in botSentMsg:
        try:
            bot.delete_message(i.chat.id, i.message_id)
        except:
            logging.info("no right to delete msg, Group:%s".format(i.chat.title))
    botSentMsg.clear()

#
# added_thread = threading.Thread(target=cronJob, name='new_added_thread')
# added_thread.start()

bot.polling(none_stop=True)
