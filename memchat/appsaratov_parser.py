import requests
from bs4 import BeautifulSoup
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def handle_text_message(bot, user_data, message):
    try:
        user_data[message.chat.id] = {"product_name": message.text}
        bot.send_message(chat_id=message.chat.id, text="Выберите город из списка:",
                         reply_markup=InlineKeyboardMarkup([
                             [InlineKeyboardButton("Саратов", callback_data='Саратов'),
                              InlineKeyboardButton("Воронеж", callback_data='Воронеж')],
                             [InlineKeyboardButton("Липецк", callback_data='Липецк')]
                         ]))
        #send_debug_message(f"{message.from_user.id} запросил антибота")
    except Exception as e:
        #send_debug_message(e)
        bot.send_message(chat_id=message.chat.id, text="Ошибка. Попробуйте еще раз.")

def handle_callback_query(bot, user_data, call):
    try:
        cities = {'Саратов': 'https://appsaratov.ru/goods/?q=',
                  'Воронеж': 'https://appvoronezh.ru/goods/?q=',
                  'Липецк': 'https://applipetsk.ru/goods/?q='}

        bot.answer_callback_query(callback_query_id=call.id)
        product_name = user_data[call.message.chat.id]["product_name"]
        url = cities[call.data] + product_name
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        products = soup.find_all("div", class_="catalog-section-item-content")
        #send_debug_message("Антибот выполняет запрос")

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
        #send_debug_message("Антибот ОК")
    except Exception as e:
        #send_debug_message(e)
        bot.send_message(chat_id=call.message.chat.id, text="Ошибка у парсера. Попробуй еще раз или сообщи Сергу")
        #send_debug_message("Ошибка парсера")