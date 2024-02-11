
import gspread
from gspread import Cell
from oauth2client.service_account import ServiceAccountCredentials
import os
import sys
import pickle
import datetime
import requests
from bs4 import BeautifulSoup
import config
from tqdm import tqdm



cred_json = config.cred_json

# Аутентификация и открытие таблицы
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
        'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_json, scope)
# client = gspread.authorize(creds)
# spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/10jbgLdWsMZ80T2mnqHj_68hW0mOOvcLD3z5-Q1sC3wo/edit#gid=2086861705')

replacement_dict = config.replacement_dict

# функция парсинга цен
def get_price(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find('span', class_='price')
    if price_element:
        price = price_element.text.replace(' ', '')
        return int(price)
    return None


# Функция для получения данных из Google Таблицы
def get_data_from_spreadsheet():
    print("Загрузка из гугл таблицы")
    # Аутентификация и открытие таблицы
    
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/10jbgLdWsMZ80T2mnqHj_68hW0mOOvcLD3z5-Q1sC3wo/edit#gid=2086861705')

    # Получение листа "Цены" таблицы
    prices_worksheet = spreadsheet.worksheet('Цены')

    # Получение всех значений из столбцов A, B, C, D, E, F, G листа "Цены"
    prices_values = prices_worksheet.get_all_values()

    # Получение листа "Остатки" таблицы
    ostatki_worksheet = spreadsheet.worksheet('Остатки')

    # Получение всех значений из столбцов A, C листа "Остатки"
    ostatki_values = ostatki_worksheet.get_all_values()
    print("Успешно")

    return {
        'prices_values': prices_values,
        'ostatki_values': ostatki_values
    }

# Функция для проверки старости файла кеша
def is_cache_expired(cache_file_path):
    if not cache_file_path:
        return True

    # Проверка, прошло ли более 30 минут с момента последнего изменения файла кеша
    current_time = datetime.datetime.now()
    cache_modified_time = datetime.datetime.fromtimestamp(os.path.getmtime(cache_file_path))
    time_difference = current_time - cache_modified_time

    return time_difference.total_seconds() > 1800  # 30 минут = 1800 секунд

# Функция для загрузки данных из файла кеша
def load_data_from_cache():
    print("Загрузка из кеша")
    try:
        with open('cache.pkl', 'rb') as cache_file:
            data = pickle.load(cache_file)
            return data
    except FileNotFoundError:
        return None

# Функция для сохранения данных в файл кеша
def save_data_to_cache(data):
    with open('cache.pkl', 'wb') as cache_file:
        pickle.dump(data, cache_file)

# Получение данных из кеша или из Google Таблицы
data = load_data_from_cache()

cache_file_path = 'cache.pkl'  # Путь к файлу кеша

if not data or is_cache_expired(cache_file_path):
    data = get_data_from_spreadsheet()
    save_data_to_cache(data)

# Ваш код для обработки данных
try:
    prices_values = data['prices_values']
    ostatki_values = data['ostatki_values']
except KeyError:
    print("Ошибка: Нет данных в кеше. Запрашиваю данные из Google Таблицы.")
    data = get_data_from_spreadsheet()
    save_data_to_cache(data)
    prices_values = data['prices_values']
    ostatki_values = data['ostatki_values']

# Получение листа "Цены" таблицы
# prices_worksheet = spreadsheet.worksheet('Цены')

# Получение всех значений из столбцов A, B, C, D, E, F, G листа "Цены"
# prices_values = prices_worksheet.get_all_values()
column_a_prices = [row[0] for row in prices_values]  # Значения из столбца A (id)
column_b_prices = [row[1] for row in prices_values]  # Значения из столбца B (vendorcode)
column_c_prices = [row[2] for row in prices_values]  # Значения из столбца C (name)
column_d_prices = [row[3] for row in prices_values]  # Значения из столбца D (price_sar)
column_e_prices = [row[4] for row in prices_values]  # Значения из столбца E (price_lip)
column_f_prices = [row[5] for row in prices_values]  # Значения из столбца F (price_vor)
column_g_prices = [row[6] for row in prices_values]  # Значения из столбца G (price_bal)
column_h_prices = [row[7] for row in prices_values]  # Значения из столбца H (stock)
column_i_prices = [row[8] for row in prices_values]  # Значения из столбца I (status)

# Создание сложного словаря на основе столбцов A, B, C, D, E, F, G листа "Цены"
prices_dict = {}
exclude = ["Другое", "Удаление"]

for i in range(len(column_a_prices)):
    item_id = column_a_prices[i]
    vendor_code = column_b_prices[i]
    item_name = column_c_prices[i]
    price_sar = column_d_prices[i]
    price_lip = column_e_prices[i]
    price_vor = column_f_prices[i]
    price_bal = column_g_prices[i]
    stock = column_h_prices[i]
    status = column_i_prices[i]

    if stock not in exclude:
        if item_id in prices_dict:
            prices_dict[item_id]['stock'].append(stock)
        else:
            prices_dict[item_id] = {
                'vendor_code': vendor_code,
                'item_name': item_name,
                'price_sar': price_sar,
                'price_lip': price_lip,
                'price_vor': price_vor,
                'price_bal' : price_bal,
                'stock': [stock][1:],
                'status': status
            }

# Получение листа "Остатки" таблицы
#ostatki_worksheet = spreadsheet.worksheet('Остатки')

# Получение всех значений из столбцов A, C листа "Остатки"
# ostatki_values = ostatki_worksheet.get_all_values()
column_a_ostatki = [row[0] for row in ostatki_values]  # Значения из столбца A (id)
column_c_ostatki = [row[2] for row in ostatki_values]  # Значения из столбца C (stock)

# Создание словаря на основе столбцов A, C листа "Остатки" с группировкой по id
ostatki_dict = {}

for i in range(len(column_a_ostatki)):
    item_id = column_a_ostatki[i]
    stock = column_c_ostatki[i]

    if item_id in ostatki_dict:
        ostatki_dict[item_id].append(stock)
    else:
        ostatki_dict[item_id] = [stock]

# Создание окончательного словаря, объединяющего информацию из словарей prices_dict и ostatki_dict
final_dict = {}

for item_id, item_info in prices_dict.items():
    if item_id in ostatki_dict:
        stocks = tuple(ostatki_dict[item_id])
        item_info['stock'] = stocks
    final_dict[item_id] = item_info

def print_item_info(item_id, item_info):
    message = ""
    message = f'🆔 {item_id}\n'
    message += f'🔢 {item_info["vendor_code"]}\n'
    message += f'🏷️ {item_info["item_name"]}\n'

    # Определение статуса товара
    status = int(item_info["status"])
    if status > 9998:
        message += '😄 В наличии\n'
    elif status > 98:
        message += '🤔 Под заказ\n'
    else:
        message += '😢 Нет на складе\n'

    # Сравнение цен с внешними сайтами
    message += compare_prices(item_info, item_info["vendor_code"])
    
    if item_info["stock"]:

        stocks = list(item_info["stock"])

        for i, stock in enumerate(stocks):

            original_value = stock
            replacement_value = replacement_dict.get(original_value)  

            if replacement_value:
                stocks[i] = replacement_value

        item_info["stock"] = tuple(stocks)

        message += f'📦: {item_info["stock"]}\n'

    else:
        message += '🕷️ Нет на складе 🕸️\n'
    message += '*ੈ✩‧₊˚༺☆༻*ੈ✩‧₊˚\n'
    return message

def compare_prices(item_info, search_query):
    sites = {
        '🆂': {
            'url': f'https://hatiko.ru/search/?query={search_query}',
            'price_key': 'price_sar'
        },
        '🆅': {
            'url': f'https://voronezh.hatiko.ru/search/?query={search_query}',
            'price_key': 'price_vor'
        },
        '🅻': {
            'url': f'https://lipetsk.hatiko.ru/search/?query={search_query}',
            'price_key': 'price_lip'
        },
        '🗿': {
            'url': f'https://balakovo.hatiko.ru/search/?query={search_query}',
            'price_key': 'price_bal'
        }
    }
    
    message = ''
    
    for site, site_info in sites.items():
        url = site_info['url']
        price_key = site_info['price_key']
        price = int(item_info[price_key])
        external_price = int(get_price(url))
        
        price_difference = abs(external_price - price)
        threshold = 0.2  # 20% threshold

        if external_price is not None and price_difference > threshold * price:
            message += f'🤯💱 проверь в мс (💰 {price} / 🌐 {external_price})\n'
        elif external_price != price:
            message += f'🌐＄ {site}: {external_price}\n'
        else:
            message += f'💰＄ {site}: {price}\n'
    
    return message

def search_items(bot, search_query, search_type, chat_id) -> str:
    bot.send_message(chat_id, "Начинаем поиск")
    count = 0
    try:
        for item_id, item_info in final_dict.items():
            if search_type == "vendor_code":
                if search_query == item_info["vendor_code"]:
                    count += 1
                    result = print_item_info(item_id, item_info)
                    bot.send_message(chat_id, result)
            elif search_type == "item_name":
                if search_query.lower() in item_info["item_name"].lower():
                    count += 1
                    result = print_item_info(item_id, item_info)
                    bot.send_message(chat_id, result)

            if count == 15:
                break

        if count < 15:
            return "Готово"
        else:
            return "Уменьши размер поиска или используй артикул"
    except Exception as e:
        return None
# Если нужно из сайта цифры узнать
def send_data(bot, message):
    search_query = message.text # получаем текст сообщения от пользователя
    for word in config.SITE_TRIGGERS: # для каждого слова в словаре
        search_query = search_query.replace (word, "")
    
    base_urls = [ # список базовых url для трех городов
    "https://hatiko.ru",
    "https://voronezh.hatiko.ru",
    "https://lipetsk.hatiko.ru",
    "https://balakovo.hatiko.ru"
]
    urls = [ # список url для трех городов
        f"https://hatiko.ru/search/?query={search_query}",
        f"https://voronezh.hatiko.ru/search/?query={search_query}",
        f"https://lipetsk.hatiko.ru/search/?query={search_query}",
        f"https://balakovo.hatiko.ru/search/?query={search_query}"
    ]
    data = [] # список для хранения данных
    for url in urls: # для каждого url
        response = requests.get(url) # делаем запрос
        soup = BeautifulSoup(response.text, "html.parser") # парсим html
        product = soup.find("a", class_="s-product-header") # находим элемент с заголовком и ссылкой
        if product: # если такой элемент есть
            title = product["title"] # получаем заголовок
            link = product["href"] # получаем ссылку
            price = soup.find("span", class_="price").text.replace(" ", "") # находим элемент с ценой и убираем пробел
            data.append((title, price, link)) # добавляем кортеж с данными в список
        else: # если такого элемента нет
            data.append(("Нет данных", "Нет данных", "Нет данных")) # добавляем кортеж с пустыми данными в список
    # формируем сообщение с данными
    for i in range(len(data)): # для каждого элемента в списке данных
        data[i] = (data[i][0], data[i][1], base_urls[i] + data[i][2]) # заменяем относительный url на абсолютный url, соединяя базовый url с относительным url
    message_text = f"🧭 {data[0][0]}\n" # заголовок одинаковый для всех городов, берем первый элемент
    message_text += f"🪙🆂 {data[0][1]}\n" # цена для Саратова
    message_text += f"🪙🆅 {data[1][1]}\n" # цена для Воронежа
    message_text += f"🪙🅻 {data[2][1]}\n" # цена для Липецка
    message_text += f"🪙🗿 {data[3][1]}\n\n" # цена для Bal
    message_text += f"🌐🆂: {data[0][2]}\n" # ссылка для Саратова
    message_text += f"🌐🆅: {data[1][2]}\n" # ссылка для Воронежа
    message_text += f"🌐🅻: {data[2][2]}" # ссылка для Липецка
    message_text += f"🌐🗿: {data[3][2]}" # ссылка для Bal
    bot.send_message(message.chat.id, message_text) # отправляем сообщение пользователю

# Определяем функцию для работы с Google таблицей
def priceup():
    
    # Создаем объект для работы с Google таблицами
    gc = gspread.authorize(creds)

    # Открываем Google таблицу по ссылке
    sheet = gc.open_by_url('https://docs.google.com/spreadsheets/d/188SpsRwhxfcf5MSD6Xtp67gZT016dw0Qp8rc4Gbysqw/edit#gid=211225988')

    # Выбираем первый лист в таблице
    worksheet = sheet.worksheet("QUERY")

    # Получаем все значения из столбца I
    values = worksheet.col_values(9)

    # Создаем словарь для хранения пар значений и цен
    dictionary = {}

    # Проходим по всем значениям в столбце I, начиная со второй строки
    # Проходим по всем значениям в столбце I, начиная со второй строки, обернув их в функцию tqdm
    # Указываем, что хотим выводить индикатор прогресса в стандартный поток вывода sys.stdout
    for value in tqdm(values[1:], file=sys.stdout):
        # Если значение не пустое и больше или равно 6000
        if value and int(value) >= 6000:
            # Формируем поисковый запрос на сайте hatiko.ru
            search_query = f'https://hatiko.ru/search/?query={value}'
            # Получаем цену с помощью функции get_price
            price = get_price(search_query)
            # Добавляем пару значение-цена в словарь
            dictionary[value] = price

    # Создаем пустой список для хранения объектов Cell
    cells = []

    # Проходим по всем парам в словаре
    for key, value in dictionary.items():
        # Находим индекс значения в столбце I
        index = values.index(key)
        # Создаем объект Cell с координатами в столбце J и значением из словаря
        cell = gspread.Cell(row=index + 1, col=10, value=value)
        # Добавляем объект Cell в список
        cells.append(cell)

    # Обновляем все ячейки в столбце J одним запросом
    worksheet.update_cells(cells)
    