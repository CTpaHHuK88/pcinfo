import psutil, datetime
import telebot
from confi import DataTelebot
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import os


bot = telebot.TeleBot(DataTelebot().TOKEN, parse_mode='HTML')

START_MESSAGE = """
/help - Помощь по командам.
Получить текущую информацию по серверу:
/work_rasp_pi - Информация по одноплатнику на работе.
/ha_rasp_pi - Информация по одноплатнику Home Assistant.
/octoprint_rasp_pi - Информация по одноплатнику Octoprint.
"""
@bot.message_handler(commands=['hi'],content_types=['text','photo'])
def start(message):
    if message.from_user.id in DataTelebot().USERS_ID:
        sent = bot.send_message(message.chat.id, 'Please describe your problem.')
        bot.register_next_step_handler(sent, msg_hi)
    else:
        bot.send_message(message.chat.id, "Access denied") 

def msg_hi(message):
    with open('problem.txt', 'w') as file:
        file.write(message.text)
    print(message.text)
    bot.send_message(message.chat.id, 'Thank you!')

# Папка для сохранения файлов (создайте заранее)
SAVE_PATH_PHOTO = 'uploaded_files/photo'

@bot.message_handler(content_types=['photo'])
def handle_file(message):
    if message.from_user.id in DataTelebot().USERS_ID:
        try:
            # Получаем информацию о файле
            if message.photo:
                file_info = bot.get_file(message.photo[-1].file_id)
                file_ext = 'jpg'
            else:
                bot.reply_to(message, "Формат файла не поддерживается.")
                return

            # Скачиваем файл
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохраняем на диск
            file_name = f"file_{message.message_id}.{file_ext}"
            file_path = os.path.join(SAVE_PATH_PHOTO, file_name)
            
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, f"Файл сохранён как: {file_name}")

        except Exception as e:
            bot.reply_to(message, f"Ошибка: {str(e)}")

    else:
        bot.send_message(message.chat.id, "Access denied") 

SAVE_PATH_DOCS = 'uploaded_files/docs'

@bot.message_handler(content_types=['document'])
def handle_doc(message):
    if message.from_user.id in DataTelebot().USERS_ID:
        try:
            # Получаем информацию о файле
            if message.document:
                file_info = bot.get_file(message.document.file_id)
                file_ext = message.document.file_name.split('.')[-1]
            else:
                bot.reply_to(message, "Формат файла не поддерживается.")
                return

            # Скачиваем файл
            downloaded_file = bot.download_file(file_info.file_path)

            # Сохраняем на диск
            file_name = f"file_{message.message_id}.{file_ext}"
            file_path = os.path.join(SAVE_PATH_DOCS, file_name)
            
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            bot.reply_to(message, f"Файл сохранён как: {file_name}")

        except Exception as e:
            bot.reply_to(message, f"Ошибка: {str(e)}")

    else:
        bot.send_message(message.chat.id, "Access denied") 

# Условие для проверки (например, температура > 25°C)
def check_condition():
    # Здесь может быть логика получения данных (API, датчик и т.д.)
    return psutil.sensors_temperatures()['cpu_thermal'][0].current

if check_condition() > 65:
    bot.send_message(996707444, "⚠️ Температура превысила 65°C!")

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if message.from_user.id in DataTelebot().USERS_ID:
        bot.send_message(message.chat.id, START_MESSAGE)
        #bot.send_message(message.chat.id, help_message)	

    else:
        bot.send_message(message.chat.id, "Access denied") 

@bot.message_handler(commands=['work_rasp_pi'])
def send_welcome(message):
    MESSAGE = f"""Система загружена:
{datetime.datetime.fromtimestamp(psutil.boot_time()).strftime("%Y-%m-%d %H:%M:%S")}
<i><b>Текущая температура процессора:</b></i>
{psutil.sensors_temperatures()['cpu_thermal'][0].current}
<i><b>Частота процессора:</b></i>
Текущая: {psutil.cpu_freq().current}
min: {psutil.cpu_freq().min}
max: {psutil.cpu_freq().max}
Количество ядер: {psutil.cpu_count()}
Загрузка проц.: {psutil.cpu_percent(interval=1)}%
"""

    if message.from_user.id in DataTelebot().USERS_ID:
        bot.send_message(message.chat.id, MESSAGE)
    else:
        bot.send_message(message.chat.id, "Access denied") 


width = len(psutil.disk_partitions())-1

i=0
while i <= width:
    print(f"{psutil.disk_partitions()[i].device}:")
    print(f"{psutil.disk_usage(psutil.disk_partitions()[i].device)}\n")
    i=i+1


bot.polling(timeout=10, long_polling_timeout = 5)