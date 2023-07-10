# Если в гугл колабе запускаешь, то сначала запусти код выше
# Импорты родных
import json
import os
import re
import sys
import traceback
import time

from sn_cutter import sn_cutter
from appsaratov_parser import asp_text_message, asp_callback_query
from usd_rate import handle_usd_rate
import megacalculator
import who_work
import phone_prices
import as_calculator

# Импорты заморских
import gspread
import telebot
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types
# from google.colab import drive # GC


# WIN Получаем путь к текущей директории скрипта
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'creds.json'), 'r') as f:
    cred_json = json.load(f)


# GC Монтируем Google Диск
# drive.mount('/content/drive')
# creds_file = '/content/drive/MyDrive/creds.json'
# with open(creds_file) as f:
#     cred_json = json.load(f)
# Открываем файл config.json и загружаем данные

with open(os.path.join(dir_path, 'config.json'), 'r') as f:
     config_data = json.load(f)

# # Получаем значение переменной bot из загруженных данных
# bot_token = config_data['bot_token']

bot = telebot.TeleBot(config_data["bot"]["token"], skip_pending=True)
ERROR_CHAT_ID = '184944023' # Кому присылать сообщения об ошибке?
DEBUG_LVL = False


# Кнопки и триггеры
welcome_message = "Я умею многое\nТы можешь мне отправить название товара или артику или нажать на эти кнопки внизу:"
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
keyboard.add(
    telebot.types.KeyboardButton("Калькулятор"),
    telebot.types.KeyboardButton("Трейдин"),
    telebot.types.KeyboardButton("SN"),
    telebot.types.KeyboardButton("Мегакалькулятор"),
    telebot.types.KeyboardButton("Кто работает"),
    telebot.types.KeyboardButton("Курс доллара")
)

# Список для триггеров вызова
# обновления кнопок
UPDATE_TRIGGERS = ["обновить", "update", "j,yjdbnm", "помощь"] 

# тестовой функции
TEST_TRIGGERS = ["test", "тест","/test"]

# калькулятора цен по карте, в рассрочку и пр
CALCULATE_TRIGGERS = ["калькулятор", "calculator", "rfkmrekznjh", "calc","кальк","сфдс","кл","cl","сд","rk", "/calculator"] 

# обрезчика серийника
SN_TRIGGERS = ["сн", "sn", "серийник","ын", "ыт","cy","/sn"] 

# трейдин-опросника
TRADEIN_TRIGGERS = ["трейдин", "tradein", "nhtqlby","tn","тн","ет","ny", "/tradein"] 

# счетчика крупных купюр
MEGACALC_TRIGGERS = ["мегакалькулятор", "мега", "mega", "mc", "ьс", "мк", "megacalc", "/megacalc"] 

# списка работающих сегодня или завтра
WW_TRIGGERS = ["кто работает", "кто", "rnj", "/whowork"] 

# курса валют
USD_RATE_COMMANDS = ['курс доллара', 'курс', 'kurs', 'rehc', '/usdrub']



# Для авторизации к гугл-таблицам
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_json, scope)
client = gspread.authorize(creds)

user_data = {}
sheet_url = "https://docs.google.com/spreadsheets/d/1ccfJRBEUib2eO58xhnGAu6T_VbfMCtVtTqRASZdqPn8/edit#gid=1724589221"
phone_prices_obj = phone_prices.PhonePrices(sheet_url ,client)

###

# Функции


# def # send_debug_message(text):
    # if DEBUG_LVL:
    #     bot.send_message(ERROR_CHAT_ID, f'DEBUG MESSAGE:\n{text}')
    # else:
    #     print(text)

def handle_exception(e):
    tb_str = traceback.format_exception(type(e), e, e.__traceback__)
    tb_str = ''.join(tb_str)
    text = f'Error occurred:\n{tb_str}'
    bot.send_message(ERROR_CHAT_ID, text)

def main():
    # send_debug_message(DEBUG_LVL)
    while True:
        try:
            bot.polling(none_stop=True, interval=0)
        except Exception as e:
            handle_exception(e)
        time.sleep(5)

## Даже не знаю зачем, но пусть будет
def contact_us(message):
    bot.send_message(message.chat.id, "Все вопросы Сергею из Балаково")

## Тестовая функция для обкатки
def test_table(message):
    global DEBUG_LVL 
    # send_debug_message(f"Переключаем на внутреннюю отладку")
    if DEBUG_LVL:
        DEBUG_LVL = False
    else:
        DEBUG_LVL = True
        # send_debug_message("Переключаем на внешнюю отладку")
        # send_debug_message(f"DEBUG_LVL: {DEBUG_LVL}")
        
# В мечтах:
# def memchat_zakaz - если цена изменилась и нужно отправить запрос складу
# ms_invoker - создание черновика заказа + отгрузки + ПКО/Вхплатежа через бота (без проводки)
# ms_sn_seeker - поиск товара по серийнику или чтобы давал линк
# ms_antibot - чтобы парсил цену с сайта и мс

# Запуск бота с кнопками

@bot.message_handler(commands=['start'])
def start_command(message): # Приветственное сообщение
    bot.send_message(message.chat.id, welcome_message)
    bot.send_message(message.chat.id, "Напиши запрос или нажми на кнопки внизу", reply_markup=keyboard)


# Ожидание сообщений, если нет нужного текста, то
# будет запускаться функция под @bot.message_handler(content_types=['text'])


@bot.message_handler(func=lambda message: message.text.lower() in UPDATE_TRIGGERS)
def update_buttons(message): # Выдает сообщение, выдавая кнопки
    bot.send_message(message.chat.id, "Обновлены кнопки", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.lower() in TEST_TRIGGERS)
def handle_test(message): # Выполнение тестовой функции
    test_table(message)

@bot.message_handler(func=lambda message: message.text == "Contact us")
def handle_contact_us(message): # Контактус
    contact_us(message)

## Калькулятор по карте, рассрочке-кредиту и кешбека
@bot.message_handler(func=lambda message: message.text.lower() in CALCULATE_TRIGGERS)
def calculate_prices(message): # Запуск калькулятора
    bot.send_message(chat_id=message.chat.id, text="Сколько за наличные:")
    bot.register_next_step_handler(message, as_calculator.process_cash_amount, bot)

## Обрезчик S у серийников
@bot.message_handler(func=lambda message: message.text.lower() in SN_TRIGGERS)
def handle_serial_number_cutter(message):
    bot.send_message(message.chat.id, "Введите серийный номер для обрезки:")
    # регистрируем следующий обработчик для ответа пользователя
    bot.register_next_step_handler(message, lambda msg: sn_cutter(msg, bot))

## Трейдин опросник
@bot.message_handler(func=lambda message: message.text.lower() in TRADEIN_TRIGGERS)
def handle_tradein(message):
    phone_prices_obj.handle_tradein(bot, message)

@bot.callback_query_handler(func=lambda call: "model:" in call.data)
def handle_model_callback(call):
    phone_prices_obj.handle_model_callback(bot ,call)

@bot.callback_query_handler(func=lambda call: "memory:" in call.data)
def handle_memory_callback(call):
    phone_prices_obj.handle_memory_callback(bot ,call)

## Кто работает сегодня или завтра
@bot.message_handler(func=lambda message: message.text.lower() in WW_TRIGGERS)
def handle_who_work(message):
    who_work.who_work(bot, message)

@bot.callback_query_handler(func=lambda call: call.data in ['today', 'tomorrow'])
def handle_ww_callback_query(call):
    who_work.ww_callback_query(bot, call, client)

# Запуск мегакалькулятора
@bot.message_handler(func=lambda message: message.text.lower() in MEGACALC_TRIGGERS)
def handle_megacalculator(message):
    megacalculator.start_megacalculator(bot, message)
    
# Запуск Курса валют
@bot.message_handler(func=lambda message: message.text.lower() in USD_RATE_COMMANDS)
def start_usd_rate(message):
    handle_usd_rate(bot, message)

# Обработчики команд
@bot.message_handler(commands=['restart'])
def handle_restart(message):
    bot.send_message(message.chat.id, "Еще раз")
    os.execl(sys.executable, sys.executable, *sys.argv)

# Если текст не соответствует ни одному варианту, то запускается основной скрипт
@bot.message_handler(content_types=['text'])
def message_handler(message):
    asp_text_message(bot, user_data, message)

@bot.callback_query_handler(func=lambda call: call.data in ['Саратов', 'Воронеж','Липецк'])
def callback_query_handler(call):
    asp_callback_query(bot, user_data, call)

# ------------------------------------------------------------------------------

if __name__ == '__main__':
    main()