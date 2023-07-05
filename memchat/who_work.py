from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime, timedelta

WW_PLACES = {
    'У': 'как Управляющий',
    'М': 'как Менеджер',
    'РБ': 'в ТЦ Рубин',
    'Р': 'на Рахова',
    'К': 'на Казачьей',
    'Ч': 'на Чернышевского',
    'И': 'как SMM'
}

# Define the inline keyboard markup
keyboard = InlineKeyboardMarkup([
    [InlineKeyboardButton(text='Сегодня', callback_data='today'),
     InlineKeyboardButton(text='Завтра', callback_data='tomorrow')]
])

def who_work(bot, message):
    # Send the message with the inline keyboard markup
    bot.send_message(chat_id=message.chat.id, text='Хочешь узнать, кто работает?\nВыберите день:', reply_markup=keyboard)

def ww_callback_query(bot, call, client):
    # Define the day offset and text based on the callback data
    day_offset = 0 if call.data == 'today' else 1
    day_text = 'Сегодня' if day_offset == 0 else 'Завтра'

    # Open the Google Sheets document by URL
    sheet = client.open_by_url('https://docs.google.com/spreadsheets/d/13KUmHtRXYbXjBE7KQ_4MFQ5VsgUYqu2heURY1y2NwiE/edit#gid=0')

    # Select the worksheet by index (0-indexed)
    worksheet = sheet.get_worksheet(0)

    # Calculate the day value
    day = datetime.now().day + day_offset

    # Get the values from the columns
    values_a = worksheet.col_values(1)[3:]
    values_b = worksheet.col_values(1 + day)[3:]

    # Generate the output text
    employee_info = []
    for a, b in zip(values_a, values_b):
        if a and a.startswith('!'):
            employee_info.append(f"\n🏢 В городе: {a[1:]}{b}\n")
        elif b and b != '':
            a = WW_PLACES.get(a, a)
            b = WW_PLACES.get(b, b)
            employee_info.append(f"👤 {a}: {b}")

    if employee_info:
        text = f"{day_text} ({(datetime.now() + timedelta(days=day_offset)).strftime('%d.%m.%Y')}) работают:\n" + '\n'.join(employee_info)
    else:
        text = f"{day_text} ({(datetime.now() + timedelta(days=day_offset)).strftime('%d.%m.%Y')}) никто не работает"

    # Send the message
    bot.send_message(chat_id=call.message.chat.id, text=text)
