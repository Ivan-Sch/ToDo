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

@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}!\n Для получения инструкции напишите /help.')

def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)

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

@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)
    if len(command) == 1:
        text = "Ошибка команды. См. /help"
    else:
        date = command[1].lower()
        task = command[2]
        if len(task) < 3:
            text = "Ошибка- задача меньше трех символов"
        else:
            add_todo(date, task)
            text = f"Задача {task} добавлена на дату {date} - {get_kategory(task)}"
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
    if len(command) == 1:
        text = "Ошибка команды. См. /help"
    else:
        date = command[1].lower()
        text = ""
        if date in tasks:
            text = date.upper() + "\n"
            for task in tasks[date]:
                text = f'{text} [] {task} {get_kategory(task)} \n'
        else:
            text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)

# Обработчик сообщений без команды
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, 'Я не понимаю эту команду.')


bot.polling(none_stop=True)