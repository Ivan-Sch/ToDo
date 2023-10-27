import sqlite3
import telebot
from telebot import custom_filters
from telebot import StateMemoryStorage
from telebot.handler_backends import StatesGroup, State
import datetime
import random
from config import TOKEN
from apscheduler.schedulers.background import BackgroundScheduler
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot(TOKEN, state_storage=state_storage, parse_mode='Markdown')
state_storage = StateMemoryStorage()
# Вставить свой токет или оставить как есть, тогда мы создадим его сами
bot = telebot.TeleBot(TOKEN, state_storage=state_storage, parse_mode='Markdown')

# Подключение к базе данных
with sqlite3.connect('bazaid.db') as conn:
    cursor = conn.cursor()
    # Создание таблицы tasks, если она не существует
    cursor.execute('''CREATE TABLE IF NOT EXISTS bazaid
                      (id,
                       task TEXT,
                       date TEXT)''')
    conn.commit()

baza_id = {}
kategory = {"Домашние дела": ["помыть посуду", "приготовить еду"],
            "Школьные дела": ["сделать уроки", "приготовить рюкзак"]}
RANDOM_TASKS = ["помыть посуду", "приготовить еду", "сделать уроки", "приготовить рюкзак"]


def get_kategory(input):
    get_kat = ""
    not_get_kat = " -@Данной категории нет"
    for i in kategory:
        if input in kategory[i]:
            get_kat = f' -@{i}'
            break
    if get_kat:
        return get_kat
    else:
        return not_get_kat


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


class PollState(StatesGroup):
    name = State()
    like = State()


class HelpState(StatesGroup):
    wait_text = State()


text_poll = "Что ты умеешь делать?"
text_button_1 = "Добавить задачу"  # Можно менять текст
text_button_2 = "Посмотреть задачу"  # Можно менять текст
text_button_3 = "Random"  # Можно менять текст
text_button_4 = "Удалить задачу"  # Можно менять текст

menu_keyboard = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_poll,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_1,
    ),
    telebot.types.KeyboardButton(
        text_button_4,
    )
)

menu_keyboard.add(
    telebot.types.KeyboardButton(
        text_button_2,
    ),
    telebot.types.KeyboardButton(
        text_button_3,
    )
)


@bot.message_handler(state="*", commands=['start'])
def start_ex(message):
    bot.send_message(
        message.chat.id,
        f'Привет, *{message.chat.first_name}*! Что будем делать?',  # Можно менять текст
        reply_markup=menu_keyboard)


@bot.message_handler(func=lambda message: text_poll == message.text)
def first(message):
    bot.send_message(message.chat.id,
                     'Супер! Я _бот_, который добавляет твои задачи на день какой ты хочешь. Как тебя зовут?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.name, message.chat.id)


@bot.message_handler(state=PollState.name)
def name(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['name'] = message.text
    bot.send_message(message.chat.id,
                     'Супер! [Нажми](https://github.com/Ivan-Sch)- тут мои рабочие коды. Как тебе?')  # Можно менять текст
    bot.set_state(message.from_user.id, PollState.like, message.chat.id)


@bot.message_handler(state=PollState.like)
def age(message):
    with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
        data['like'] = message.text
    bot.send_message(message.chat.id, 'Спасибо за использование меня!',
                     reply_markup=menu_keyboard)  # Можно менять текст
    bot.delete_state(message.from_user.id, message.chat.id)


# Создаем уникальные идентификаторы для кнопок
BUTTON_ONE_ID = 'button_one_id'
BUTTON_TWO_ID = 'button_two_id'
BUTTON_THREE_ID = 'button_three_id'

BUTTON_FOUR_ID = 'button_four_id'
BUTTON_FIVE_ID = 'button_five_id'
BUTTON_SIX_ID = 'button_six_id'

BUTTON_SEVEN_ID = 'button_seven_id'
BUTTON_EIGHTH_ID = 'button_eighth_id'
BUTTON_NINE_ID = 'button_nine_id'

# Создаем инлайн-кнопки
button_today_1 = InlineKeyboardButton('Сегодня', callback_data=BUTTON_ONE_ID)
button_tomorrow_1 = InlineKeyboardButton('Завтра', callback_data=BUTTON_TWO_ID)
button_other_1 = InlineKeyboardButton('Другая дата', callback_data=BUTTON_THREE_ID)

button_today_2 = InlineKeyboardButton('Сегодня', callback_data=BUTTON_FOUR_ID)
button_tomorrow_2 = InlineKeyboardButton('Завтра', callback_data=BUTTON_FIVE_ID)
button_other_2 = InlineKeyboardButton('Другая дата', callback_data=BUTTON_SIX_ID)

button_today_3 = InlineKeyboardButton('Сегодня', callback_data=BUTTON_SEVEN_ID)
button_tomorrow_3 = InlineKeyboardButton('Завтра', callback_data=BUTTON_EIGHTH_ID)
button_other_3 = InlineKeyboardButton('Другая дата', callback_data=BUTTON_NINE_ID)
# Создаем клавиатуру с кнопками
keyboard1_add = InlineKeyboardMarkup()
keyboard1_add.add(button_today_1)
keyboard1_add.add(button_tomorrow_1)
keyboard1_add.add(button_other_1)

keyboard2_show = InlineKeyboardMarkup()
keyboard2_show.add(button_today_2)
keyboard2_show.add(button_tomorrow_2)
keyboard2_show.add(button_other_2)

keyboard3_dell = InlineKeyboardMarkup()
keyboard3_dell.add(button_today_3)
keyboard3_dell.add(button_tomorrow_3)
keyboard3_dell.add(button_other_3)


# Обработчик нажатий на кнопки
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    # Кнопки для добавления задачи
    if call.data == BUTTON_ONE_ID:
        # Выполняем действие для кнопки 1
        bot.send_message(call.message.chat.id, 'Сегодня')
        get_date("Сегодня", call.message.chat.id)
    elif call.data == BUTTON_TWO_ID:
        # Выполняем действие для кнопки 2
        bot.send_message(call.message.chat.id, 'Завтра')
        get_date("Завтра", call.message.chat.id)
    elif call.data == BUTTON_THREE_ID:
        # Выполняем действие для кнопки 3
        bot.send_message(call.message.chat.id, 'Укажите дату:')
        bot.register_next_step_handler(call.message, get_custom_date, call.message.chat.id)
    # Кнопки для показа задач
    elif call.data == BUTTON_FOUR_ID:
        # Выполняем действие для кнопки 4
        bot.send_message(call.message.chat.id, 'Сегодня')
        bot.send_message(call.message.chat.id, get_tasks('Сегодня', call.message.chat.id))
        # get_tasks("Сегодня", call.message.chat.id)
    elif call.data == BUTTON_FIVE_ID:
        # Выполняем действие для кнопки 5
        bot.send_message(call.message.chat.id, 'Завтра')
        bot.send_message(call.message.chat.id, get_tasks('Завтра', call.message.chat.id))
    elif call.data == BUTTON_SIX_ID:
        # Выполняем действие для кнопки 6
        bot.send_message(call.message.chat.id, 'Укажите дату:')
        bot.register_next_step_handler(call.message, get_custom_date, call.message.chat.id, "show")
    # Кнопки для удаления
    elif call.data == BUTTON_SEVEN_ID:
        # Выполняем действие для кнопки 4
        bot.send_message(call.message.chat.id, 'Сегодня')
        get_tasks_com_4('Сегодня', call.message.chat.id)
        # bot.register_next_step_handler(call.message, get_tasks_com_4, call.message.chat.id)
        # get_tasks("Сегодня", call.message.chat.id)
    elif call.data == BUTTON_EIGHTH_ID:
        # Выполняем действие для кнопки 5
        bot.send_message(call.message.chat.id, 'Завтра')
        get_tasks_com_4('Завтра', call.message.chat.id)
    elif call.data == BUTTON_NINE_ID:
        # Выполняем действие для кнопки 6
        bot.send_message(call.message.chat.id, 'Укажите дату:')
        bot.register_next_step_handler(call.message, get_custom_date, call.message.chat.id, "dell")


def get_custom_date(message, id, fl=None):
    if type(message) is telebot.types.Message:
        date = message.text.lower()
    else:
        date = message.lower()
    if fl is None:
        bot.send_message(message.chat.id, f'Вы указали дату {date}')
        get_date(date, id)
    elif fl == "dell":
        get_tasks_com_4(date, id)
    elif fl == "show":
        bot.send_message(id, get_tasks(date, id))


# Добавление задачи - add
@bot.message_handler(func=lambda message: text_button_1 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, text='Выбери день:', reply_markup=keyboard1_add)


# Обработчик следующего шага - получение даты
def get_date(date, id):
    if type(date) is telebot.types.Message:
        date = date.text.lower()
    else:
        date = date.lower()

    if not is_valid_date(date):
        text = "Ошибка команды."
        bot.send_message(id, text)
    else:
        date = get_date_ddmmyyyy(date)
        # bot.send_message(id, f'Укажите, какую задачу вы хотите добавить на дату *"{date}"*:')
        bot.register_next_step_handler(
            bot.send_message(id, f'Укажите, какую задачу вы хотите добавить на дату *"{date}"*:'), save_task, date, id)


# Функция для сохранения задачи в базе данных
def save_task(message, date, id):
    if type(message) is telebot.types.Message:
        task = message.text
    else:
        task = message
    with sqlite3.connect('bazaid.db') as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO bazaid (id, task, date) VALUES (?, ?, ?)", (id, task, date))
        conn.commit()
    bot.send_message(id, f'Задача *"{task}"* добавлена на _"{date}"_.')


# Показ задачи - show
@bot.message_handler(func=lambda message: text_button_2 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, text='Выбери день:', reply_markup=keyboard2_show)


# Функция вывода результата показа дня
def get_tasks(message, id):
    if type(message) is telebot.types.Message:
        date = message.text.lower()
    else:
        date = message.lower()
    if not is_valid_date(date):
        text = "Ошибка команды."
    else:
        date = get_date_ddmmyyyy(date)
        with sqlite3.connect('bazaid.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT task FROM bazaid WHERE date=? AND id=?", (date, id))
            tasks = cursor.fetchall()
            taskss = [task[0] for task in tasks]
        if len(taskss) == 0:
            text = f'Задач на эту дату нет.'
        else:
            text = f'*{get_date_slova(date).upper()}* \n'
            for i in range(len(taskss)):
                text = f'{text}{i + 1}) *{taskss[i]}* _{get_kategory(taskss[i])}_ \n'
    return text


# Random задачи на сегодня
@bot.message_handler(func=lambda message: text_button_3 == message.text)
def help_command(message):
    date = "сегодня"
    task = random.choice(RANDOM_TASKS)
    save_task(task, get_date_ddmmyyyy(date), message.chat.id)  # Можно менять текст


# Удаление задачи - dell
@bot.message_handler(func=lambda message: text_button_4 == message.text)
def help_command(message):
    bot.send_message(message.chat.id, text='Выбери день:', reply_markup=keyboard3_dell)


def get_tasks_com_4(message, id):
    print(message)
    date = message
    get_task = get_tasks(date, id)
    if get_task in ["Ошибка команды.", "Задач на эту дату нет."]:
        bot.send_message(id, get_task)
    else:
        bot.send_message(id, get_task)
        bot.register_next_step_handler(bot.send_message(id, "Укажите номер:"), del_task, date, id)


def del_task(message, date, id):
    number_del = message.text
    id_user = message.chat.id
    task_del = get_tasks(date, id_user).split(")")[int(number_del)].split("*")[1]
    # Подключение к базе данных
    with sqlite3.connect('bazaid.db') as conn:
        cursor = conn.cursor()
        # Создание таблицы tasks, если она не существует
        cursor.execute("DELETE FROM bazaid WHERE id = ? AND task = ?", (id_user, task_del))
        conn.commit()

    bot.send_message(message.chat.id, "Удаление прошло успешно!")


def update_tasks():
    yesterday = (datetime.date.today() - datetime.timedelta(days=1)).strftime('%d.%m.%Y')
    # yesterday = "23.10.2023"
    # Удаление задач завершенных вчера
    with sqlite3.connect('bazaid.db') as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM bazaid WHERE date=?", (yesterday,))
        conn.commit()


# Запускаем планировщик задач
scheduler = BackgroundScheduler()
scheduler.add_job(update_tasks, 'interval', minutes=30)  # Запускать каждые 30 минут
scheduler.start()


# Обработка команды /delete_expired_tasks
@bot.message_handler(commands=['update_tasks'])
def delete_expired_tasks_command(message):
    update_tasks()


bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.add_custom_filter(custom_filters.TextMatchFilter())

bot.infinity_polling()
