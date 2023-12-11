import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from itertools import groupby
import pickle
import datetime
import requests
from bs4 import BeautifulSoup

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'creds.json'), 'r') as f:
    cred_json = json.load(f)

# Аутентификация и открытие таблицы
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_json, scope)
# client = gspread.authorize(creds)
# spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/10jbgLdWsMZ80T2mnqHj_68hW0mOOvcLD3z5-Q1sC3wo/edit#gid=2086861705')

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
                'stock': [stock][1:]
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

# Запрос ввода от пользователя
search_query = input("Введите поисковой запрос: ")

if search_query.isdigit():
    # Поиск по vendorcode
    count = 0  # Счетчик итераций
    for item_id, item_info in final_dict.items():
        if item_info["vendor_code"] == search_query:
            count += 1
            print(f'ID: {item_id}')
            print(f'Vendor Code: {item_info["vendor_code"]}')
            print(f'Name: {item_info["item_name"]}')

            # Сравнение цен с сайтами
            price_sar = int(item_info["price_sar"])
            price_vor = int(item_info["price_vor"])
            price_lip = int(item_info["price_lip"])

            url_sar = f'https://hatiko.ru/search/?query={search_query}'
            url_vor = f'https://voronezh.hatiko.ru/search/?query={search_query}'
            url_lip = f'https://lipetsk.hatiko.ru/search/?query={search_query}'

            price_sar_ext = int(get_price(url_sar))
            price_vor_ext = int(get_price(url_vor))
            price_lip_ext = int(get_price(url_lip))

            if price_sar_ext is not None and price_sar_ext != price_sar:
                print(f'External SAR Price: {price_sar_ext}')
            elif price_sar_ext is not None:
                print(f'Price SAR: {price_sar_ext}')

            if price_lip_ext is not None and price_lip_ext != price_lip:
                print(f'External LIP Price: {price_lip_ext}')
            elif price_lip_ext is not None:
                print(f'Price LIP: {price_lip_ext}')

            if price_vor_ext is not None and price_vor_ext != price_vor:
                print(f'External VOR Price: {price_vor_ext}')
            elif price_vor_ext is not None:
                print(f'Price VOR: {price_vor_ext}')

            if item_info["stock"]:
                print(f'Stock: {item_info["stock"]}')
            else:
                print('Stock: Нет на складе')
            print('------------------')

            if count == 5:
                choice = input(f"Показаны первые 5 совпадений. Продолжить? (да/нет): ")
                if choice.lower() != "да":
                    break
else:
    # Поиск по item_name (поиск подстроки)
    count = 0  # Counter for iterations
    for item_id, item_info in final_dict.items():
        if search_query.lower() in item_info["item_name"].lower():
            count += 1
            print(f'ID: {item_id}')
            print(f'Vendor Code: {item_info["vendor_code"]}')
            print(f'Name: {item_info["item_name"]}')
            # print(f'Price SAR: {item_info["price_sar"]}')
            # print(f'Price LIP: {item_info["price_lip"]}')
            # print(f'Price VOR: {item_info["price_vor"]}')
            if item_info["stock"]:
                print(f'Stock: {item_info["stock"]}')
            else:
                print('Stock: Нет на складе')
            print('------------------')
            
            if count == 5:
                choice = input(f"Показаны первые 5 совпадений. Продолжить? (да/нет): ")
                if choice.lower() != "да":
                    break