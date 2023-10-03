import telebot

token = "xx"

bot = telebot.TeleBot(token)
my_name = "Иван"
HELP = """
/help - справка.
/add - добавить задачу.
/show - напечатать все наши задачи.
/random - добавить случайную задачу на дату Сегодня"""

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

bot.polling(none_stop=True)