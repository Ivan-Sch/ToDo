import telebot

import random
token = "xx"

bot = telebot.TeleBot(token)
RANDOM_TASKS = ["Записаться на курс", "Записаться на госуслуги", "Покормить кота", "Помыть машину"]

HELP = """
/help - справка.
/add - добавить задачу.
/show - напечатать все наши задачи.
/random - добавить случайную задачу на дату Сегодня"""

tasks = {}
baza_id = {}

@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.id}!\n Для получения инструкции напишите /help.')


def add_todo(date, task, id):
    if id not in baza_id:
        baza_id[id] = {}
    if date in baza_id[id]:
        baza_id[id][date].append(task)
    else:
        baza_id[id][date] = []
        baza_id[id][date].append(task)

kategory = {"Домашние дела": ["помыть посуду", "приготовить еду"], "Школьные дела": ["сделать уроки", "приготовить рюкзак"]}
def get_kategory(input):
    get_kat = ""
    not_get_kat = "@данной категории нет"
    for i in kategory:
        if input in kategory[i]:
            get_kat = f'@{i}'
            break
    if get_kat:
        return get_kat
    else:
        return not_get_kat

@bot.message_handler(commands=["help"])
def help(message):
    bot.send_message(message.chat.id, HELP)

all_dates = ["сегодня", "завтра"]

@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)
    if len(command) == 1 or command[1].lower() not in all_dates:
        text = "Ошибка команды. См. /help"
    else:
        date = command[1].lower()
        task = command[2]
        if len(task) < 3:
            text = "Ошибка- задача меньше трех символов"
        else:
            add_todo(date, task, message.chat.id)
            text = f"Задача {task} добавлена на дату {date} - {get_kategory(task)}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["rez"])
def rez(message):
    bot.send_message(message.chat.id, str(baza_id))

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "сегодня"
    task = random.choice(RANDOM_TASKS)
    add_todo(date, task, message.chat.id)
    text = f"Задача {task} добавлена на дату {date}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["show", "print"])
def show(message):
    command = message.text.split(maxsplit=1)
    if len(command) == 1 or command[1].lower() not in all_dates:
        text = "Ошибка команды. См. /help"
    else:
        date = command[1].lower()
        text = ""
        if message.chat.id not in baza_id:
            baza_id[message.chat.id] = {}
        if date in baza_id[message.chat.id]:
            text = date.upper() + "\n"
            for task in baza_id[message.chat.id][date]:
                text = f'{text} [] {task} {get_kategory(task)} \n'
        else:
            text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)

# Обработчик сообщений без команды
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, 'Я не понимаю эту команду.')


bot.polling(none_stop=True)