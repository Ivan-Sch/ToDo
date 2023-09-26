HELP = """
help - справка.
add - добавить задачу.
show - напечатать все наши задачи.
random - добавлять случайную задачу на дату Сегодня"""

RANDOM_TASK = "Записаться в парикмахерскую"

tasks = {}
today = []
tomorrow = []
other = []

run = True

def add_todo(date, task):
    if date in tasks:
        tasks[date].append(task)
    else:
        tasks[date] = []
        tasks[date].append(task)
        print(f"Задача {task} добавлена на дату {date}!")

while run:
    command = input("Введите команду: ")
    if command == "help":
        print(HELP)
    elif command == "show":
        date = input("Введите дату для отоброжения списка задач: ")
        if date in tasks:
            for task in tasks[date]:
                print("- ", task)
        else:
            print("Такой даты нет")

    elif command == "add":
        date = input("Введите дату выполнения задачи: ")
        task = input("Введите название задачи: ")
        add_todo(date,task)
    elif command == "random":
       add_todo("Сегодня", RANDOM_TASK)
    elif command == "exit":
        print("Спасибо за использование! До свидания!")
        break
    else:
        print("Неизвестная команда!")
        break

print("До свидания!")
