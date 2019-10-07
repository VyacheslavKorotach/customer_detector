import telebot
import time
import os

bot_token = os.environ["EXCHANGE_BOT_TOKEN"]
bot = telebot.TeleBot(bot_token)

users = []


@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Привет":
        bot.send_message(message.from_user.id, "Привет, чем я могу тебе помочь? " + str(message.from_user.id))
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Напиши 'Привет'")
    else:
        bot.send_message(message.from_user.id, "Я тебя не понимаю. Напиши /help.")
    users.append(message.from_user.id)


while True:
#    bot.send_message(563646664, "Start there")
    bot.send_message(-1001440639497, "Start in channel")
    time.sleep(10)

# bot.polling(none_stop=False, interval=0, timeout=20)
#bot.polling(none_stop=True, interval=0)
