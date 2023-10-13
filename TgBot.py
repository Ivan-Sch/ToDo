import telebot
import datetime
import random
token = "xx"

bot = telebot.TeleBot(token)
RANDOM_TASKS = ["Записаться на курс", "Записаться на госуслуги", "Покормить кота", "Помыть машину"]

HELP = """
/help - справка.
/add - добавить задачу.
""Пример: /add сегодня помыть посуду
/show - напечатать все наши задачи.
""Пример: /show сегодня
/random - добавить случайную задачу на дату Сегодня"""

tasks = {}
baza_id = {}

@bot.message_handler(commands=['start'])
def say_hi(message):
    bot.send_message(message.chat.id, f'Привет, {message.chat.first_name}!\n Для получения инструкции напишите /help.')

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

def is_valid_date(date_string):
    if date_string in ["сегодня", "завтра"]:
        if date_string == "сегодня":
            date_string = datetime.date.today().strftime('%d.%m.%Y')
        else:
            date_string = str((datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%Y'))
    try:
        datetime.datetime.strptime(date_string, '%d.%m.%Y')
        return True
    except ValueError:
        return False

def get_date_slova(date):
    if date == datetime.date.today().strftime('%d.%m.%Y'):
        return "сегодня"
    if date == str((datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%Y')):
        return "завтра"
    else:
        return date


def get_date_ddmmyyyy(date):
    if date == "сегодня":
        return datetime.date.today().strftime('%d.%m.%Y')
    if date == "завтра":
        return str((datetime.date.today() + datetime.timedelta(days=1)).strftime('%d.%m.%Y'))
    else:
        return date

@bot.message_handler(commands=["add"])
def add(message):
    command = message.text.split(maxsplit=2)
    if len(command) <= 2 or not is_valid_date(command[1].lower()):
        text = "Ошибка команды. См. /help"
    else:
        # date = get_date(command[1].lower())
        date = get_date_ddmmyyyy(command[1].lower())
        task = command[2]
        if len(task) < 3:
            text = "Ошибка- задача меньше трех символов"
        else:
            add_todo(date, task, message.chat.id)
            text = f"Задача {task} добавлена на дату {get_date_slova(date)} - {get_kategory(task)}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["rez"])
def rez(message):
    bot.send_message(message.chat.id, str(baza_id))

@bot.message_handler(commands=["random"])
def random_add(message):
    date = "сегодня"
    task = random.choice(RANDOM_TASKS)
    add_todo(get_date_ddmmyyyy(date), task, message.chat.id)
    text = f"Задача {task} добавлена на дату {date}"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["show", "print"])
def show(message):
    command = message.text.split(maxsplit=1)
    if len(command) == 1 or not is_valid_date(command[1].lower()):
        text = "Ошибка команды. См. /help"
    else:
        # date = command[1].lower()
        date = get_date_ddmmyyyy(command[1].lower())

        text = ""
        if message.chat.id not in baza_id:
            baza_id[message.chat.id] = {}
        if date in baza_id[message.chat.id]:
            text = get_date_slova(date).upper() + "\n"
            for task in baza_id[message.chat.id][date]:
                text = f'{text} [---> {task} {get_kategory(task)} \n'
        else:
            text = "Задач на эту дату нет"
    bot.send_message(message.chat.id, text)

@bot.message_handler(commands=["time"])
def my_time(message):
    bot.send_message(message.chat.id, datetime.datetime.now())

# Обработчик сообщений без команды
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    bot.send_message(message.chat.id, 'Я не понимаю эту команду.')


def del_last_date():
    last_date = str((datetime.date.today() - datetime.timedelta(days=1)).strftime('%d.%m.%Y'))
    for id in baza_id:
        if last_date in baza_id[id]:
            del baza_id[id][last_date]

# Запускаем планировщик задач
scheduler = BackgroundScheduler()
scheduler.add_job(del_last_date, 'interval', minutes=30)  # Запускать каждые 30 минут
scheduler.start()

# Обработка команды /delete_expired_tasks
@bot.message_handler(commands=['del_last_date'])
def delete_expired_tasks_command(message):
    del_last_date()


print(datetime.datetime.now())

bot.polling(none_stop=True)