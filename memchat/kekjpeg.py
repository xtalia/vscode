# # Импортируем необходимые библиотеки
# import config
# import gspread
# import json
# from oauth2client.service_account import ServiceAccountCredentials
# import telebot

# # Указываем область доступа к API
# scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

# # Получаем ключ доступа к API из файла JSON
# credentials = ServiceAccountCredentials.from_json_keyfile_name('creds.json', scope)

# # Авторизуемся в API с помощью ключа
# gc = gspread.authorize(credentials)

# # Открываем гугл таблицу по ссылке
# sh = gc.open_by_url('https://docs.google.com/spreadsheets/d/1ccfJRBEUib2eO58xhnGAu6T_VbfMCtVtTqRASZdqPn8/edit#gid=1724589221')

# # Выбираем лист с данными
# worksheet = sh.worksheet('Для заполнения iPhone')

# # Получаем все значения из листа в виде списка списков
# values = worksheet.get_all_values()

# # Создаем пустой словарь для хранения данных в формате JSON
# data = {}

# # Проходим по всем строкам, начиная со второй (первая - заголовки столбцов)
# for row in values[1:]:
#     # Получаем название модели из столбца A
#     model = row[0]
#     # Проверяем, есть ли уже такая модель в словаре данных
#     if model not in data:
#         # Если нет, то создаем для нее пустой список
#         data[model] = []
#     # Создаем словарь для хранения данных одной строки, кроме названия модели
#     record = {}
#     # Заполняем словарь значениями из столбцов, используя их названия в качестве ключей
#     record['memory'] = row[1] # Столбец B - память
#     record['ideal_price'] = row[2] # Столбец C - идеальная цена
#     record['screen_replacement'] = row[3] # Столбец D - замена экрана
#     record['battery_wear'] = row[4] # Столбец E - износ аккумулятора
#     record['battery_replacement'] = row[5] # Столбец F - замена аккумулятора
#     record['device_only'] = row[6] # Столбец G - только устройство
#     record['device_box'] = row[7] # Столбец H - устройство+коробка
#     record['back_cover_replacement'] = row[8] # Столбец I - замена задней крышки
#     # Добавляем словарь в список данных для соответствующей модели
#     data[model].append(record)

# # Преобразуем словарь данных в JSON-строку с отступами для удобства чтения
# json_data = json.dumps(data, indent=4)

# # Выводим JSON-строку на экран

# # Можем также сохранить JSON-строку в файл
# with open('tradeiniphone.json', 'w') as f:
#     f.write(json_data)
    
# import kekjpeg
# # Импортируем необходимые библиотеки

# # Создаем словарь для хранения данных пользователя
# user_data = {}

# # Создаем словарь для хранения данных из гугл таблицы
# data = {}

# # Загружаем данные из файла JSON, который мы получили из гугл таблицы
# with open('data.json', 'r') as f:
#     data = json.load(f)

# # Создаем словарь с вопросами и вариантами ответов
# questions = {
#     'model': {
#         'text': 'Какая у вас модель iPhone?',
#         'options': list(data.keys())
#     },
#     'memory': {
#         'text': 'Какой у вас объем памяти?',
#         'options': lambda user_id: [record['memory'] for record in data[user_data[user_id]['model']]]
#     },
#     'battery': {
#         'text': 'Какая у вас емкость аккумулятора?',
#         'options': ['меньше 85%', 'меньше 91%', 'больше 91%']
#     },
#     'complect': {
#         'text': 'Какой у вас комплект?',
#         'options': ['Только устройство', 'Устройство+коробка', 'Полный']
#     },
#     'back_cover': {
#         'text': 'Цела ли у вас задняя крышка?',
#         'options': ['Да', 'Нет']
#     },
#     'screen': {
#         'text': 'Цел ли у вас экран?',
#         'options': ['Да', 'Нет']
#     },
#     'condition': {
#         'text': 'Какое у вас внешнее состояние?',
#         'options': ['Отлично/Хорошо', 'Среднее', 'Плохое']
#     }
# }

# # Создаем список с порядком вопросов
# order = ['model', 'memory', 'battery', 'complect', 'back_cover', 'screen', 'condition']



# # Создаем функцию для обработки команды /start
# @bot.message_handler(commands=['tn'])
# def start(message):
#     # Получаем идентификатор пользователя
#     user_id = message.from_user.id
#     # Создаем пустой словарь для хранения данных пользователя
#     user_data[user_id] = {}
#     # Отправляем приветственное сообщение
#     bot.send_message(user_id, 'Здравствуйте, это бот для опросника по трейдину iPhone. Я задам вам несколько вопросов и посчитаю цену, которую вы можете получить за ваше устройство.')
#     # Переходим к первому вопросу
#     ask_question(user_id, 0)

# # Создаем функцию для задания вопроса по индексу
# def ask_question(user_id, index):
#     # Получаем ключ вопроса из списка
#     key = order[index]
#     # Получаем текст вопроса из словаря
#     text = questions[key]['text']
#     # Получаем варианты ответов из словаря
#     options = questions[key]['options']
#     # Если варианты ответов - функция, то вызываем ее с идентификатором пользователя
#     if callable(options):
#         options = options(user_id)
#     # Создаем список кнопок с вариантами ответов
#     buttons = []
#     for option in options:
#         buttons.append(telebot.types.InlineKeyboardButton(text=option, callback_data=option))
#     # Создаем клавиатуру из кнопок
#     keyboard = telebot.types.InlineKeyboardMarkup()
#     keyboard.add(*buttons)
#     # Отправляем вопрос с клавиатурой
#     bot.send_message(user_id, text, reply_markup=keyboard)


# # Создаем глобальную переменную для счетчика вопросов
# question_counter = 0

# # Создаем функцию для обработки ответа на вопрос
# @bot.callback_query_handler(func=lambda call: True)
# def answer_question(call):
#     # Получаем идентификатор пользователя
#     user_id = call.from_user.id
#     # Получаем текст ответа
#     answer = call.data

#     # Проверяем, есть ли такой ответ в словаре вопросов
#     for key, value in questions.items():
#         options = value['options']  # Получаем варианты ответов из словаря
#         if callable(options):
#             options = options(user_id)

#         if answer in options:
#             # Если есть, то сохраняем ответ в данных пользователя
#             user_data[user_id][key] = answer
#             # Увеличиваем счетчик вопросов
#             global question_counter
#             question_counter += 1
#             # Проверяем, есть ли еще вопросы
#             if question_counter < len(order):
#                 # Если есть, то переходим к следующему вопросу
#                 ask_question(user_id, question_counter)
#             else:
#                 # Если нет, то завершаем опрос и выводим результат
#                 finish(user_id)
#             # Прерываем цикл
#             break



# # Создаем функцию для завершения опроса и вывода результата
# def finish(user_id):
#     # Получаем данные пользователя
#     data = user_data[user_id]
#     print(data)
#     # Получаем модель и память
#     model = data['model'] # Используем 'model' в качестве ключа для словаря data
#     memory = data['memory']
#     # Находим соответствующую запись в данных из гугл таблицы
#     record = None
#     record = data['model']
#     record = data['memory']
    
#     # for r in data[model]: # Используем data[model] в качестве источника данных по модели
#     #     if r['memory'] == memory:
#     #         record = r
#     #         break
#     # Если не нашли, то выводим сообщение об ошибке
#     if record is None:
#         bot.send_message(user_id, 'Извините, я не смог найти данные для вашей модели и памяти.')
#         return
#     # Иначе, начинаем расчет цены
#     # Берем идеальную цену из записи
#     price = int(record['ideal_price'])
#     # Учитываем емкость аккумулятора
#     if data['battery'] == 'меньше 85%':
#         price += int(record['battery_replacement'])
#     elif data['battery'] == 'меньше 91%':
#         price += int(record['battery_wear'])
#     # Учитываем комплект
#     if data['complect'] == 'Только устройство':
#         price += int(record['device_only'])
#     elif data['complect'] == 'Устройство+коробка':
#         price += int(record['device_box'])
#     # Учитываем целостность задней крышки
#     if data['back_cover'] == 'Нет':
#         price += int(record['back_cover_replacement'])
#     # Учитываем целостность экрана
#     if data['screen'] == 'Нет':
#         price += int(record['screen_replacement'])
#     # Учитываем внешнее состояние
#     if data['condition'] == 'Среднее':
#         price -= 1000
#     elif data['condition'] == 'Плохое':
#         price -= 2000
#     # Отправляем результат пользователю
#     bot.send_message(user_id, f'{model} - {memory}\nЦена в трейдин до {price} рублей.')