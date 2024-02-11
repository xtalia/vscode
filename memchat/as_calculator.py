def process_cash_amount(message, bot):
    try:
        # send_debug_message(f"{message.from_user.id} запросил Калькулятор")
        cash = float(message.text.strip())

        # Расчет по карте, рассрочку, кредиту, кешбеку
        # qr_price = round(cash * 1.015, -2)  - 10
        qr_price = round(cash * 1.01501, -2) -10
        card_price = round(cash * 1.0301, -2) -10
        rassrochka_price = round(cash * 1.0701, -2) -10
        credit_price = round(cash * 1.1801, -2) -10
        cashback_amount = round(cash * 0.01)

        # Оформление сообщения
        output = "Стоимость: {:.0f} рублей с учетом скидки за оплату наличными\n\n".format(cash)
        output += "* QR = {:.0f} рублей\n".format(qr_price)
        output += "* по карте = {:.0f} рублей\n\n".format(card_price)
        output += "** в рассрочку = {:.0f} рублей (от {:.0f} руб. на 6 месяцев)\n".format(rassrochka_price, rassrochka_price / 6)
        output += "** в кредит = {:.0f} рублей + % Банка".format(credit_price)
        # 20% годовых на 36 мес = 60% | 40 годовых на 36 = 120%
        output += "(от {:.0f} - {:.0f} руб. сроком до 36 месяцев)\n".format(credit_price * 1.60 / 36, credit_price * 2.2 / 36)
        output += "** %Банка ~ от 20 до 40% годовых (точные условия может предоставить только менеджер)\n"
        output += "Кешбек = {:.0f} внутренними рублями\n (через 2 недели, если закажете самостоятельно на сайте)".format(cashback_amount)

        # Вывод пользователю
        bot.send_message(chat_id=message.chat.id, text=output)
        # send_debug_message("Калькулятор ОК")
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text="Сломался калькулятор, что-то пошло не так (Только цифры)")
        # send_debug_message("Калькулятор Ошибка")
     
def process_original_price(message, bot):
    try:
        original_price = float(message.text)

        # Запрашиваем скидку
        bot.send_message(message.chat.id, "Введите скидку:")
        bot.register_next_step_handler(message, lambda msg: process_discount(msg, bot, original_price))
    except:
        bot.send_message(chat_id=message.chat.id, text="Сломался калькулятор, что-то пошло не так (Только цифры)")
        

def process_discount(message, bot, original_price):
        try:
            discount = float(message.text)

            # Вычисляем процент скидки и сумму со скидкой
            discounted_price = original_price - discount
            discount_percentage = 100 - discounted_price / (original_price * 0.01)
            

            # Формируем сообщение с результатами
            result_message = f"Изначальная цена: {int(original_price)}\n"
            result_message += f"Скидка: {discount}\n"
            result_message += f"Процент скидки: {discount_percentage}\n"
            result_message += f"Сумма со скидкой: {discounted_price}"

            # Отправляем результат пользователю
            bot.send_message(message.chat.id, result_message)
        except:
            bot.send_message(chat_id=message.chat.id, text="Сломался калькулятор, что-то пошло не так (Только цифры)")
        