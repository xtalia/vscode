from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta

WW_PLACES = {
    'Voronezh': 'Воронеж',
    'Kursk': 'Курск',
    'Belgorod': 'Белгород',
    'Lipetsk': 'Липецк',
    'Tambov': 'Тамбов',
    'Orel': 'Орел',
    'Bryansk': 'Брянск',
    'Kursk': 'Курск',
    'Vladimir': 'Владимир',
    'Tula': 'Тула',
    'Ryazan': 'Рязань',
}

def work_message(bot, client, message):
    # define the inline keyboard markup
    keyboard = InlineKeyboardMarkup()
    today_button = InlineKeyboardButton(text='Сегодня', callback_data='today')
    tomorrow_button = InlineKeyboardButton(text='Завтра', callback_data='tomorrow')
    keyboard.row(today_button, tomorrow_button)

    # send the message with the inline keyboard markup
    bot.send_message(chat_id=message.chat.id, text='Хочешь узнать, кто работает?\nВыберите день:', reply_markup=keyboard)

# define the callback query handler function
def callback_query(bot, client, call):
    if call.data == 'today':
        day_offset = 0
        day_text = 'Сегодня'
    else:
        day_offset = 1
        day_text = 'Завтра'
    
    # open the Google Sheets document by URL
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/13KUmHtRXYbXjBE7KQ_4MFQ5VsgUYqu2heURY1y2NwiE/edit#gid=0')

    # select the worksheet by index (0-indexed)
    worksheet = sheet.get_worksheet(0)

    day = datetime.now().day + day_offset

    # Получаем данные из 1 столбца со списком сотрудников и городов (которые помечены символом !) и из столбца B-AF соответсвующий запросу (сегодня или завтра)
    values_a = [value.strip() for value in worksheet.col_values(1)[3:]]
    values_b = [value.strip() for value in worksheet.col_values(1 + day)[3:]]

    # get the current date and time
    now = datetime.now()

    # print the values from the 1st and 2nd columns
    a_values = []
    for a, b in zip(values_a, values_b):
        if a is not None:
            if a.startswith('!'):
                a_values.append(f"\n🏢 В городе: {a[1:]}{b}\n")
            elif b is not None and b != '':
                a = WW_PLACES.get(a, a)
                b = WW_PLACES.get(b, b)
                a_values.append(f"👤 {a}: {b}")

    # format the output
    if a_values:
        text = f"{day_text} ({(now + timedelta(days=day_offset)).strftime('%d.%m.%Y')}) работают:\n" + '\n'.join(a_values)
    else:
        text = f"{day_text} ({(now + timedelta(days=day_offset)).strftime('%d.%m.%Y')}) никто не работает"

    # send the message
    bot.send_message(chat_id=call.message.chat.id, text=text)