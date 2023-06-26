# Экспериментальная версия
# Если в гугл колабе запускаешь, то сначала запусти код выше
import telebot
from bs4 import BeautifulSoup
import requests
from telebot import types
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
# from google.colab import drive # GC
import json
import re
import os

bot = telebot.TeleBot('6089036388:AAFACsFqem3-v5j5HDWWsuBglQbA1sGpER8', skip_pending=True)

# Переменные и кнопки
welcome_message = "Я умею многое\nТы можешь мне отправить название товара или артику или нажать на эти кнопки внизу:"
keyboard = telebot.types.ReplyKeyboardMarkup(row_width=2)
keyboard.add(telebot.types.KeyboardButton("Калькулятор"))
keyboard.add(telebot.types.KeyboardButton("Трейдин"))
keyboard.add(telebot.types.KeyboardButton("SN"))
keyboard.add(telebot.types.KeyboardButton("Мегакалькулятор"))

# WIN Получаем путь к текущей директории скрипта
dir_path = os.path.dirname(os.path.realpath(__file__))
# WIN Открываем файл creds.json в режиме чтения
with open(os.path.join(dir_path, 'creds.json'), 'r') as f:
    # Загружаем данные из файла
    cred_json = json.load(f)

# GC Монтируем Google Диск
# drive.mount('/content/drive')

# GC Указываем путь к файлу creds.json
# creds_file = 'creds.json'

# GC Открываем файл с учетными данными
# with open(creds_file) as f:
#    cred_json = json.load(f)

scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive', 'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_json, scope)
client = gspread.authorize(creds)

# -----------------------------------------------------------------------------

# Класс, который вытаскивает данные из таблицы трейдина и потом выдает результат по запросу

class PhonePrices:
    def __init__(self, sheet_url, client):
        self.sheet_url = sheet_url
        self.client = client
        self.sheet_name = "Для заполнения iPhone"
        self.data = None
        self.headers = None
        self.model_index = None
        self.memory_index = None
        self.price_index = None
        self.screen_index = None
        self.battery_index = None
        self.device_only_index = None
        self.device_box_index = None
        self.back_cover_index = None

        self._import_data()
        self.models = self._get_models()

    def _import_data(self):
        # scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive.readonly"]
        # keyfile_json = json.dumps(self.keyfile_dict)
        # creds = ServiceAccountCredentials.from_json_keyfile_dict(json.loads(keyfile_json), scope)
        # client = gspread.authorize(self.creds)

        sheet = self.client.open_by_url(self.sheet_url).worksheet(self.sheet_name)
        self.data = sheet.get_all_values()
        self.headers = [header.strip() for header in self.data[0]]
        self.model_index = self.headers.index("Модель")
        self.memory_index = self.headers.index("Память")
        self.price_index = self.headers.index("Идеальная цена")
        self.screen_index = self.headers.index("Замена экрана")
        self.battery_index = self.headers.index("Замена аккумулятора")
        self.device_only_index = self.headers.index("Только устройство")
        self.device_box_index = self.headers.index("устройство+коробка")
        self.back_cover_index = self.headers.index("Замена задней крышки")

    def _get_models(self):
        models = {}
        for row in self.data[1:]:
            model = row[self.model_index]
            memory = row[self.memory_index]
            if model not in models:
                models[model] = [memory]
            elif memory not in models[model]:
                models[model].append(memory)
        return models

    def get_memory_options(self, model):
        if model not in self.models:
            raise ValueError(f"Модель '{model}' не найдена")
        return self.models[model]

    def get_price(self, model, memory, options=None):
        for row in self.data[1:]:
            if row[self.model_index] == model and row[self.memory_index] == memory:
                # Рассчитать стоимость телефона без дополнительных опций
                price = float(row[self.price_index])
                if options is None:
                    return price

                # Рассчитать стоимость телефона с дополнительными опциями
                total_price = price
                for option in options:
                    if option == "Замена экрана":
                        total_price += float(row[self.screen_index])
                    elif option == "Замена аккумулятора":
                        total_price += float(row[self.battery_index])
                    elif option == "Только устройство":
                        total_price += float(row[self.device_only_index])
                    elif option == "устройство+коробка":
                        total_price += float(row[self.device_box_index])
                    elif option == "Замена задней крышки":
                        total_price += float(row[self.back_cover_index])
                return total_price

        # Если не найдено соответствующей строки, вернуть None
        return None

# вызов данных у класса
sheet_url = "https://docs.google.com/spreadsheets/d/1ccfJRBEUib2eO58xhnGAu6T_VbfMCtVtTqRASZdqPn8/edit#gid=1724589221"
phone_prices = PhonePrices(sheet_url, client)
user_data = {}
###

# -----------------------------------------------------------------------------
# Функции
# -----------------------------------------------------------------------------

################### Калькулятор по карте или в рассрочку по таксе AppSaratov ##
def process_cash_amount(message): 
    try:
        print("Кто-то запросил Калькулятор")
        cash = float(message.text.strip())

        # Calculate prices and discounts
        card_price = round(cash * 1.03 / 10) * 10 - 10
        rassrochka_price = round(cash * 1.08 / 10) * 10 - 10
        credit_price = round(cash * 1.03 / 10) * 10 - 10
        cashback_amount = round(cash * 0.005)

        # Generate output message
        output = "Стоимость: {:.0f} рублей с учетом скидки за оплату наличными\n".format(cash)
        output += "* по карте = {:.0f} рублей\n\n".format(card_price)
        output += "** в рассрочку = {:.0f} рублей (от {:.0f} руб. на 6 месяцев)\n".format(rassrochka_price, rassrochka_price / 6)
        output += "** в кредит = {:.0f} рублей + % Банка".format(credit_price)
        output += "(от {:.0f} - {:.0f} руб. сроком до 18 месяцев)\n".format(credit_price * 0.20 / 18, credit_price * 0.40 / 18)
        output += "** оформить в рассрочку или кредит возможно в нашем магазине по ул. Чернышевского 89 и в ТЦ Рубин (Высокая 12А)\n\n"
        output += "Кешбек = {:.0f} внутренними рублями\n (через 2 недели, если закажете самостоятельно на сайте)".format(cashback_amount)

        # Send output message to Telegram chat
        bot.send_message(chat_id=message.chat.id, text=output)
        print("Калькулятор ОК")
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text="Сломался калькулятор, что-то пошло не так (Только цифры)")
        print("Калькулятор Ошибка")
###

def memchat_zakaz(message):
  pass

def contact_us(message):
    bot.send_message(message.chat.id, "Here is how you can contact us: phone number, email address, or other ways.")

def test_table(message): # Тестовая функция
    bot.send_message(message.chat.id, "Тут ничего нет")

def sn_cutter(message): # Убирает первую букву (полезно для checkoverage)
    # проверяем первую букву сообщения
    if message.text and message.text[0] == "S" or message.text[0] == "Ы":
        text = message.text[1:]
        # здесь можно выполнить другие действия с текстом сообщения
        bot.send_message(message.chat.id, text)
    else:
        bot.send_message(message.chat.id, f"Это точно серийный номер? ({message.text})")

# В мечтах:
# def memchat_zakaz - если цена изменилась и нужно отправить запрос складу
# ms_invoker - создание черновика заказа + отгрузки + ПКО/Вхплатежа через бота (без проводки)
# ms_sn_seeker - поиск товара по серийнику или чтобы давал линк
# ms_antibot - чтобы парсил цену с сайта и мс
# def memchat_zakaz - если цена изменилась и нужно отправить запрос складу
# hr_memes - выводить список работников на сегодняшний день


###################################################### Запуск бота с кнопками ##
@bot.message_handler(commands=['start'])
def start_command(message): # Приветственное сообщение
    bot.send_message(message.chat.id, welcome_message)
    bot.send_message(message.chat.id, "Напиши запрос или нажми на кнопки внизу", reply_markup=keyboard)

# -----------------------------------------------------------------------------
# Ожидание сообщений, если нет нужного текста, то
# будет запускаться функция под @bot.message_handler(content_types=['text'])
# -----------------------------------------------------------------------------

@bot.message_handler(func=lambda message: message.text.lower() in ["обновить", "update", "j,yjdbnm", "помощь"])
def update_buttons(message): # Выдает сообщение, выдавая кнопки
    bot.send_message(message.chat.id, "Обновлены кнопки", reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text.lower() in ["test", "тест","/test"])
def handle_test(message): # Выполнение тестовой функции
    test_table(message)

@bot.message_handler(func=lambda message: message.text == "Contact us")
def handle_contact_us(message): # Контактус
    contact_us(message)

@bot.message_handler(func=lambda message: message.text.lower() in ["калькулятор", "calculator", "rfkmrekznjh", "calc","кальк","сфдс","кл","cl","сд","rk", "/calculator"])
def calculate_prices(message): # Запуск калькулятора

    # Ask user for cash amount
    bot.send_message(chat_id=message.chat.id, text="Сколько за наличные:")
    bot.register_next_step_handler(message, process_cash_amount)

@bot.message_handler(func=lambda message: message.text.lower() in ["сн", "sn", "серийник","ын", "ыт","cy","/sn"])
def handle_serial_number_cutter(message):
    bot.send_message(message.chat.id, "Введите серийный номер для обрезки:")
    # регистрируем следующий обработчик для ответа пользователя
    bot.register_next_step_handler(message, sn_cutter)


############################################################ Трейдин опросник ##

@bot.message_handler(func=lambda message: message.text.lower() in ["трейдин", "tradein", "nhtqlby","tn","тн","ет","ny", "/tradein"])
def handle_tradein(message):
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
    if len(memory_options) == 0:
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
    text = call.message.text.strip() #.text.split(":")[1].strip()
    pattern = r"'(.*?)'"
    model = re.search(pattern, text).group(1)
    print(model)
    memory = call.data.split(":")[1]
    options = []
    if call.message.text.lower() == "да":
        options.append("Замена экрана")
    message = bot.send_message(call.message.chat.id, "Введите емкость аккумулятора (в процентах):")
    bot.register_next_step_handler(message, handle_battery_capacity, phone_prices, model, memory, options) #, call.message
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
    print(model)
    print(memory)
    print(options)

    total_price = phone_prices.get_price(model, memory, options) #=options
    response = f"* Модель: {model}, Память: {memory}\n"
    # response += f"Емкость аккумулятора: {message.text}%\n" if message.text.isdigit() else ""
    response += f"* Цена в Трейдин: до {total_price:.0f} рублей\n"
    response += f"*На что повлияла цена:\n {options}\n*Если состояние неудовлетворительное,\nто уточни у сервисных менеджеров"
    bot.send_message(message.chat.id, response)

### Конец опросника

######################## Бот, который считает число купюр и показывает сумму. ##
@bot.message_handler(func=lambda message: message.text.lower() in ["мегакалькулятор", "мега", "mega", "mc", "ьс", "мк", "megacalc", "/megacalc"])
def start_megacalculator(message):
    bot.send_message(message.chat.id, "Привет! Я мегакалькулятор. Сколько у вас купюр номиналом 5000?")
    bot.register_next_step_handler(message, calculate_5000)

def calculate_5000(message):
    try:
        count_5000 = int(message.text)
        bot.send_message(message.chat.id, "Сколько купюр номиналом 2000?")
        bot.register_next_step_handler(message, calculate_2000, count_5000)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")

def calculate_2000(message, count_5000):
    try:
        count_2000 = int(message.text)
        bot.send_message(message.chat.id, "Сколько купюр номиналом 1000?")
        bot.register_next_step_handler(message, calculate_1000, count_5000, count_2000)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")

def calculate_1000(message, count_5000, count_2000):
    try:
        count_1000 = int(message.text)
        bot.send_message(message.chat.id, "Сколько купюр номиналом 500?")
        bot.register_next_step_handler(message, calculate_500, count_5000, count_2000, count_1000)
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")

def calculate_500(message, count_5000, count_2000, count_1000):
    try:
        count_500 = int(message.text)
        total_sum = count_5000 * 5000 + count_2000 * 2000 + count_1000 * 1000 + count_500 * 500
        bot.send_message(message.chat.id, f"5000 х {count_5000}\n2000 x {count_2000}\n1000 x {count_1000}\n500 x {count_500}\nИтого: {total_sum}")
    except ValueError:
        bot.send_message(message.chat.id, "Пожалуйста, введите число.")

### Конец мегакальулятора

############################################################ Основная функция ##

@bot.message_handler(content_types=['text'])
def handle_text_message(message):
    ask_city(message)

def ask_city(message):
    try:
        user_data[message.chat.id] = {"product_name": message.text}
        text = "Выберите город из списка:"
        keyboard = [
            [InlineKeyboardButton("Саратов", callback_data='Саратов'),
             InlineKeyboardButton("Воронеж", callback_data='Воронеж')],
            [InlineKeyboardButton("Липецк", callback_data='Липецк')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        bot.send_message(chat_id=message.chat.id, text=text, reply_markup=reply_markup)
    except Exception as e:
        print(e)
        bot.send_message(chat_id=message.chat.id, text="Ошибка. Попробуйте еще раз.")

@bot.callback_query_handler(func=lambda call: True)
def handle_callback_query(call):
    try:
        if call.data == 'Саратов':
            city = "https://appsaratov.ru/goods/?q="
        elif call.data == 'Воронеж':
            city = "https://appvoronezh.ru/goods/?q="
        elif call.data == 'Липецк':
            city = "https://applipetsk.ru/goods/?q="
        bot.answer_callback_query(callback_query_id=call.id)
        product_name = user_data[call.message.chat.id]["product_name"]
        url = city + product_name
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("div", class_="catalog-section-item-content")
        print("Антибот выполняет запрос")

        if products:
            for product in products:
                name_element = product.find("a", class_="catalog-section-item-name-wrapper intec-cl-text-hover")
                name = name_element.text.strip() if name_element else "Без имени (мс)"

                availability_element = product.find("div", class_="catalog-section-item-quantity")
                availability = availability_element.text.strip() if availability_element else "Статус неизвестен"

                price_element = product.find("span", attrs={"data-role": "item.price.discount"})
                price = price_element.text.strip() if price_element else "Цена неизвестна (мс)"

                message_body = f"{name}\n{availability}\n{price}\n"
                message_body += f"Не проходим*\nАктуально {call.data}? Есть у нас. Когда привезете? Если под заказ - без предоплаты сможем? Клиент в магазине\n"

                bot.send_message(chat_id=call.message.chat.id, text=message_body)
        else:
            bot.send_message(chat_id=call.message.chat.id, text="Не найдено - попробуй еще раз")
        print("Антибот ОК")
    except Exception as e:
        print(e)
        bot.send_message(chat_id=call.message.chat.id, text="Ошибка у парсера. Попробуй еще раз или сообщи Сергу")
        print("Ошибка парсера")

# -----------------------------------------------------------------------------

if __name__ == '__main__': # Запуск бота
    print("Запуск бота")
    #bot.polling(none_stop=True, interval=0)
    try:
        bot.polling(none_stop=True, interval=0)
    except:
        print("Ошибка у бота - перезапусти без эксепшена")
        bot.polling(none_stop=True, interval=0)