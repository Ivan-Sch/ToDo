import telebot
import random
token = "xx"

bot = telebot.TeleBot(token)
RANDOM_TASKS = ["Записаться на курс", "Записаться на госуслуги", "Покормить кота", "Помыть машину"]
my_name = "Иван"
HELP = """
/help - справка.
/add - добавить задачу.
/show - напечатать все наши задачи.
/random - добавить случайную задачу на дату Сегодня"""

tasks = {}

def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)
@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)
    date = command[1].lower()
    task = command[2]
    add_todo(date, task)
    text = f"Задача {task} добавлена на дату {date}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "сегодня"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task)
    text = f"Задача {task} добавлена на дату {date}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["show", "print"])
def show(message):
    command = message.text.split(maxsplit=1)
    date = command[1].lower()
    text = ""
    if date in tasks:
        text = date.upper() + "\n"
        for task in tasks[date]:
            text = text + "[] " + task + "\n"
    else:
        text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)





bot.polling(none_stop=True)