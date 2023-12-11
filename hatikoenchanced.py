import gspread
from oauth2client.service_account import ServiceAccountCredentials
import os
import json
from itertools import groupby
import datetime
import pickle

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, 'creds.json'), 'r') as f:
    cred_json = json.load(f)

# Аутентификация и открытие таблицы
scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive',
         'https://www.googleapis.com/auth/spreadsheets']
creds = ServiceAccountCredentials.from_json_keyfile_dict(cred_json, scope)
client = gspread.authorize(creds)
spreadsheet = client.open_by_url('https://docs.google.com/spreadsheets/d/10jbgLdWsMZ80T2mnqHj_68hW0mOOvcLD3z5-Q1sC3wo/edit#gid=2086861705')

# Получение листа "Цены" таблицы
prices_worksheet = spreadsheet.worksheet('Цены')

# Получение всех значений из столбцов A, B, C, D, E, F, G листа "Цены"
prices_values = prices_worksheet.get_all_values()
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
                'stock': [stock]
            }

# Получение листа "Остатки" таблицы
ostatki_worksheet = spreadsheet.worksheet('Остатки')

# Получение всех значений из столбцов A, C листа "Остатки"
ostatki_values = ostatki_worksheet.get_all_values()
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

# Проверка, является ли введенный запрос числом
if search_query.isdigit():
    # Поиск по vendorcode
    for item_id, item_info in final_dict.items():
        if item_info["vendor_code"] == search_query:
            print(f'ID: {item_id}')
            print(f'Vendor Code: {item_info["vendor_code"]}')
            print(f'Name: {item_info["item_name"]}')
            print(f'Price SAR: {item_info["price_sar"]}')
            print(f'Price LIP: {item_info["price_lip"]}')
            print(f'Price VOR: {item_info["price_vor"]}')
            print(f'Stock: {item_info["stock"]}')
            print('------------------')
else:
    # Поиск по item_name (поиск подстроки)
    for item_id, item_info in final_dict.items():
        if search_query in item_info["item_name"]:
            print(f'ID: {item_id}')
            print(f'Vendor Code: {item_info["vendor_code"]}')
            print(f'Name: {item_info["item_name"]}')
            print(f'Price SAR: {item_info["price_sar"]}')
            print(f'Price LIP: {item_info["price_lip"]}')
            print(f'Price VOR: {item_info["price_vor"]}')
            print(f'Stock: {item_info["stock"]}')
            print('------------------')