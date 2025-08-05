import psutil, datetime
import telebot
from confi import DataTelebot
import time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove


bot = telebot.TeleBot(DataTelebot().TOKEN, parse_mode='HTML')

START_MESSAGE = """
/help - Помощь по командам.
Получить текущую информацию по серверу:
/work_rasp_pi - Информация по одноплатнику на работе.
/ha_rasp_pi - Информация по одноплатнику Home Assistant.
/octoprint_rasp_pi - Информация по одноплатнику Octoprint.
"""

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