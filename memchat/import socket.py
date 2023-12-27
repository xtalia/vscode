import socket
import requests
from bs4 import BeautifulSoup
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import urllib.parse

# Устанавливаем параметры подключения к Google API
# scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
# creds = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)
# client = gspread.authorize(creds)

# Получаем экземпляр таблицы
# sheet = client.open('Prices').sheet1

def get_price(url):
    """Получение цены со страницы"""
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    price_element = soup.find('span', class_='price')
    if price_element:
        price = price_element.text.replace(' ', '')
        return int(price)
    return None

def stop():
    """Остановка цикла обновления"""
    print("Цикл обновления остановлен")

def start(force=False):
    """Запуск цикла обновления"""
    print("Цикл обновления запущен")
    # Здесь можно написать код для цикла обновления
    if force:
        print("Обязательное обновление данных")

def status():
    """Получение статуса обновления данных"""
    updated = 0
    # Здесь можно написать код для проверки количества измененных значений
    print(f"Количество измененных значений: {updated}")

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 22000))
server_socket.listen()

while True:
    conn, addr = server_socket.accept()
    data = conn.recv(1024).decode()
    if not data:
        break
    parsed_data = urllib.parse.parse_qs(data)
    if 'command' in parsed_data:
        command = parsed_data['command'][0]
        if command == "stop":
            stop()
        elif command == "start":
            start()
        elif command == "start_force":
            start(force=True)
        elif command == "status":
            status()
        else:
            print("Unknown command")
    else:
        print("Command not specified in request")
    conn.close()