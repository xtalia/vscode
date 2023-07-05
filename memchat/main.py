# Экспериментальная версия
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

# Импорты заморских
import gspread
import telebot
from oauth2client.service_account import ServiceAccountCredentials
from telebot import types
# from google.colab import drive # GC


bot = telebot.TeleBot('6057005343:AAHWzzPQ-IshPv_Z5y4uPKuHWE160TqpaeM', skip_pending=True)
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

# Список для триггеров 
UPDATE_TRIGGERS = ["обновить", "update", "j,yjdbnm", "помощь"] # обновления кнопок

TEST_TRIGGERS = ["test", "тест","/test"] # тестовой функции

CALCULATE_TRIGGERS = ["калькулятор", "calculator", "rfkmrekznjh", "calc","кальк","сфдс","кл","cl","сд","rk", "/calculator"] # калькулятора цен по карте, в рассрочку и пр

SN_TRIGGERS = ["сн", "sn", "серийник","ын", "ыт","cy","/sn"] # обрезчика серийника

TRADEIN_TRIGGERS = ["трейдин", "tradein", "nhtqlby","tn","тн","ет","ny", "/tradein"] # трейдин-опросника

MEGACALC_TRIGGERS = ["мегакалькулятор", "мега", "mega", "mc", "ьс", "мк", "megacalc", "/megacalc"] # счетчика крупных купюр

WW_TRIGGERS = ["кто работает", "кто", "rnj", "/whowork"] # вызова списка работающих сегодня или завтра

USD_RATE_COMMANDS = ['курс доллара', 'курс', 'kurs', 'rehc', '/usdrub']

# WIN Получаем путь к текущей директории скрипта
dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'creds.json'), 'r') as f:
    cred_json = json.load(f)

# GC Монтируем Google Диск
# drive.mount('/content/drive')
# creds_file = '/content/drive/MyDrive/creds.json'
# with open(creds_file) as f:
#     cred_json = json.load(f)

# Для авторизации к гугл-таблицам
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_json, scope)
client = gspread.authorize(creds)


# -----------------------------------------------------------------------------

# Класс, который вытаскивает данные из таблицы трейдина и потом выдает результат по запросу

class PhonePrices:
    def __init__(self, sheet_url, client):
        # Initialize instance variables
        self.sheet_url = sheet_url
        self.client = client
        self.sheet_name = "Для заполнения iPhone"

        # Import data from Google Sheets
        self.data = self._import_data()

        # Get column indices for relevant fields
        self.model_index = self.headers.index("Модель")
        self.memory_index = self.headers.index("Память")
        self.price_index = self.headers.index("Идеальная цена")
        self.screen_index = self.headers.index("Замена экрана")
        self.battery_index = self.headers.index("Замена аккумулятора")
        self.device_only_index = self.headers.index("Только устройство")
        self.device_box_index = self.headers.index("устройство+коробка")
        self.back_cover_index = self.headers.index("Замена задней крышки")

        # Get models and their memory options
        self.models = self._get_models()

    def _import_data(self):
        # Open the Google Sheets document by URL
        sheet = self.client.open_by_url(self.sheet_url).worksheet(self.sheet_name)

        # Get all values from the sheet
        data = sheet.get_all_values()

        # Strip whitespace from headers
        self.headers = [header.strip() for header in data[0]]

        # Return the data
        return data

    def _get_models(self):
        models = {}
        # Loop through all data rows except for the header row
        for row in self.data[1:]:
            model = row[self.model_index]
            memory = row[self.memory_index]
            # If the model hasn't been added to the dictionary yet, add it with its first memory option
            models.setdefault(model, [memory])
            # Otherwise, add the memory option to the existing model's list of options
            if memory not in models[model]:
                models[model].append(memory)
        return models

    def get_memory_options(self, model):
        # Check if the model exists in the data
        if model not in self.models:
            raise ValueError(f"Модель '{model}' не найдена")

        # Return the list of memory options for the given model
        return self.models[model]

    def get_price(self, model, memory, options=None):
        # Loop through all data rows except for the header row
        for row in self.data[1:]:
            # Check if the row corresponds to the given model and memory
            if row[self.model_index] == model and row[self.memory_index] == memory:
                # Calculate the base price of the phone without any additional options
                price = float(row[self.price_index])
                if options is None:
                    return price

                # Calculate the total price of the phone with the additional options
                total_price = price
                option_indices = {
                    "Замена экрана": self.screen_index,
                    "Замена аккумулятора": self.battery_index,
                    "Только устройство": self.device_only_index,
                    "устройство+коробка": self.device_box_index,
                    "Замена задней крышки": self.back_cover_index
                }
                for option in options:
                    total_price += float(row[option_indices[option]])
                return total_price

        # If no matching row is found, return None
        return None

# вызов данных у класса
sheet_url = "https://docs.google.com/spreadsheets/d/1ccfJRBEUib2eO58xhnGAu6T_VbfMCtVtTqRASZdqPn8/edit#gid=1724589221"
phone_prices = PhonePrices(sheet_url, client)
user_data = {}
###

# -----------------------------------------------------------------------------

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

## Калькулятор по карте или в рассрочку по таксе AppSaratov
def process_cash_amount(message): 
    try:
        # send_debug_message(f"{message.from_user.id} запросил Калькулятор")
        cash = float(message.text.strip())

        # Расчет по карте, рассрочку, кредиту, кешбеку
        card_price = round(cash * 1.03 / 10) * 10 - 10
        rassrochka_price = round(cash * 1.08 / 10) * 10 - 10
        credit_price = round(cash * 1.03 / 10) * 10 - 10
        cashback_amount = round(cash * 0.005)

        # Оформление сообщения
        output = "Стоимость: {:.0f} рублей с учетом скидки за оплату наличными\n".format(cash)
        output += "* по карте = {:.0f} рублей\n\n".format(card_price)
        output += "** в рассрочку = {:.0f} рублей (от {:.0f} руб. на 6 месяцев)\n".format(rassrochka_price, rassrochka_price / 6)
        output += "** в кредит = {:.0f} рублей + % Банка".format(credit_price)
        output += "(от {:.0f} - {:.0f} руб. сроком до 18 месяцев)\n".format(credit_price * 0.20 / 18, credit_price * 0.40 / 18)
        output += "** оформить в рассрочку или кредит возможно в нашем магазине по ул. Чернышевского 89 и в ТЦ Рубин (Высокая 12А)\n\n"
        output += "Кешбек = {:.0f} внутренними рублями\n (через 2 недели, если закажете самостоятельно на сайте)".format(cashback_amount)

        # Вывод пользователю
        bot.send_message(chat_id=message.chat.id, text=output)
        # send_debug_message("Калькулятор ОК")
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text="Сломался калькулятор, что-то пошло не так (Только цифры)")
        # send_debug_message("Калькулятор Ошибка")

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
        

## Обрезчик серийника
# def sn_cutter(message):
#     if message.text and message.text[0] in "SЫ":
#         sn = message.text[1:]
#         bot.send_message(message.chat.id, sn)
#     else:
#         bot.send_message(message.chat.id, f"Это точно серийный номер? ({message.text})")

# В мечтах:
# def memchat_zakaz - если цена изменилась и нужно отправить запрос складу
# ms_invoker - создание черновика заказа + отгрузки + ПКО/Вхплатежа через бота (без проводки)
# ms_sn_seeker - поиск товара по серийнику или чтобы давал линк
# ms_antibot - чтобы парсил цену с сайта и мс

# -----------------------------------------------------------------------------
# Запуск бота с кнопками

@bot.message_handler(commands=['start'])
def start_command(message): # Приветственное сообщение
    bot.send_message(message.chat.id, welcome_message)
    bot.send_message(message.chat.id, "Напиши запрос или нажми на кнопки внизу", reply_markup=keyboard)

# -----------------------------------------------------------------------------
# Ожидание сообщений, если нет нужного текста, то
# будет запускаться функция под @bot.message_handler(content_types=['text'])
# -----------------------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text.lower() in UPDATE_TRIGGERS)
def update_buttons(message): # Выдает сообщение, выдавая кнопки
    bot.send_message(message.chat.id, "Обновлены кнопки", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.lower() in TEST_TRIGGERS)
def handle_test(message): # Выполнение тестовой функции
    test_table(message)

@bot.message_handler(func=lambda message: message.text == "Contact us")
def handle_contact_us(message): # Контактус
    contact_us(message)

@bot.message_handler(func=lambda message: message.text.lower() in CALCULATE_TRIGGERS)
def calculate_prices(message): # Запуск калькулятора

    # Ask user for cash amount
    bot.send_message(chat_id=message.chat.id, text="Сколько за наличные:")
    bot.register_next_step_handler(message, process_cash_amount)

@bot.message_handler(func=lambda message: message.text.lower() in SN_TRIGGERS)
def handle_serial_number_cutter(message):
    bot.send_message(message.chat.id, "Введите серийный номер для обрезки:")
    # регистрируем следующий обработчик для ответа пользователя
    bot.register_next_step_handler(message, lambda msg: sn_cutter(msg, bot))

## Трейдин опросник

@bot.message_handler(func=lambda message: message.text.lower() in TRADEIN_TRIGGERS)
def handle_tradein(message):
    # send_debug_message(f"{message.from_user.id} запросил Трейдин")
    models = phone_prices.models.keys()
    model_buttons = types.InlineKeyboardMarkup(row_width=2)
    for model in models:
        button = types.InlineKeyboardButton(text=model, callback_data=f"model:{model}")
        model_buttons.add(button)
    bot.send_message(message.chat.id, "Выберите модель:", reply_markup=model_buttons)

@bot.callback_query_handler(func=lambda call: "model:" in call.data)
def handle_model_callback(call):
    model = call.data.split(":")[1]
    memory_options = phone_prices.get_memory_options(model)
    if not memory_options:
        bot.send_message(call.message.chat.id, f"Для модели '{model}' не найдено вариантов памяти")
        return
    memory_buttons = types.InlineKeyboardMarkup(row_width=2)
    for memory in memory_options:
        button = types.InlineKeyboardButton(text=memory, callback_data=f"memory:{memory}")
        memory_buttons.add(button)
    bot.send_message(call.message.chat.id, f"Выберите память для модели '{model}':", reply_markup=memory_buttons)
    bot.answer_callback_query(callback_query_id=call.id)

@bot.callback_query_handler(func=lambda call: "memory:" in call.data)
def handle_memory_callback(call):
    model_pattern = r"'(.*?)'"
    model = re.search(model_pattern, call.message.text).group(1)
    memory = call.data.split(":")[1]
    options = []
    message = bot.send_message(call.message.chat.id, "Введите емкость аккумулятора (в процентах):")
    bot.register_next_step_handler(message, handle_battery_capacity, phone_prices, model, memory, options)
    bot.answer_callback_query(callback_query_id=call.id)

def handle_battery_capacity(message, phone_prices, model, memory, options):
    try:
        battery_capacity = int(message.text)
        if battery_capacity < 85:
            options.append("Замена аккумулятора")
        message = bot.send_message(message.chat.id, "Только устройство? (да / нет):")
        bot.register_next_step_handler(message, handle_device_only, phone_prices, model, memory, options)
    except ValueError:
        bot.send_message(message.chat.id, "Емкость аккумулятора должна быть числом. Пожалуйста, введите число:")

def handle_device_only(message, phone_prices, model, memory, options):
    if message.text.lower() == "да":
        options.append("Только устройство")
    message = bot.send_message(message.chat.id, "Устройство+коробка? (да / нет):")
    bot.register_next_step_handler(message, handle_display, phone_prices, model, memory, options)

def handle_display(message, phone_prices, model, memory, options):
    if message.text.lower() == "да":
        options.append("устройство+коробка")
    message = bot.send_message(message.chat.id, "Замена экрана (да / нет):")
    bot.register_next_step_handler(message, handle_device_box, phone_prices, model, memory, options)

def handle_device_box(message, phone_prices, model, memory, options):
    if message.text.lower() == "да":
        options.append("Замена экрана")
    message = bot.send_message(message.chat.id, "Замена задней крышки? (да / нет):")
    bot.register_next_step_handler(message, handle_back_cover, phone_prices, model, memory, options)

def handle_back_cover(message, phone_prices, model, memory, options):
    if message.text.lower() == "да":
        options.append("Замена задней крышки")
    total_price = phone_prices.get_price(model, memory, options)
    response = f"* Модель: {model}, Память: {memory}\n"
    response += f"* Цена в Трейдин: до {total_price:.0f} рублей\n"
    response += f"*На что повлияла цена:\n {options}\n*Если состояние неудовлетворительное,\nто уточни у сервисных менеджеров"
    bot.send_message(message.chat.id, response)
    # send_debug_message(f"{message.from_user.id} Трейдин ОК")

## Конец опросника

## Кто работает сегодня или завтра



@bot.message_handler(func=lambda message: message.text.lower() in WW_TRIGGERS)
def handle_who_work(message):
    who_work.who_work(bot, message)

@bot.callback_query_handler(func=lambda call: call.data in ['today', 'tomorrow'])
def handle_ww_callback_query(call):
    who_work.ww_callback_query(bot, call, client)

## Конец

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