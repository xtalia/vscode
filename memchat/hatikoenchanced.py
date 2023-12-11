
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import time
import json
import pickle
import datetime
import requests
from bs4 import BeautifulSoup
from telebot import types
import config

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'creds.json'), 'r') as f:
    cred_json = json.load(f)

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
column_g_prices = [row[6] for row in prices_values]  # Значения из столбца G (stock)
column_h_prices = [row[7] for row in prices_values]  # Значения из столбца H (status)

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
    stock = column_g_prices[i]
    status = column_h_prices[i]

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
            message += f'🤯💱 проверь в мс (💰 {price} \ 🌐 {external_price})\n'
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



# Запрос ввода от пользователя
# search_query = input("Введите поисковой запрос: ")

# if search_query.isdigit():
#    search_by_vendor_code(search_query)
# else:
#    search_by_item_name(search_query)