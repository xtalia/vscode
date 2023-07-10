def process_cash_amount(message, bot):
    try:
        # send_debug_message(f"{message.from_user.id} запросил Калькулятор")
        cash = float(message.text.strip())

        # Расчет по карте, рассрочку, кредиту, кешбеку
        card_price = round(cash * 1.03, -2)  - 10
        rassrochka_price = round(cash * 1.08, -2)  - 10
        credit_price = round(cash * 1.03, -2)  - 10
        cashback_amount = round(cash * 0.005)

        # Оформление сообщения
        output = "Стоимость: {:.0f} рублей с учетом скидки за оплату наличными\n".format(cash)
        output += "* по карте = {:.0f} рублей\n\n".format(card_price)
        output += "** в рассрочку = {:.0f} рублей (от {:.0f} руб. на 6 месяцев)\n".format(rassrochka_price, rassrochka_price / 6)
        output += "** в кредит = {:.0f} рублей + % Банка".format(credit_price)
        output += "(от {:.0f} - {:.0f} руб. сроком до 18 месяцев)\n".format(credit_price * 0.20 / 18, credit_price * 0.40 / 18)
        output += "** оформить в рассрочку или кредит возможно в нашем магазине по ул. Чернышевского 89 и в ТЦ Рубин (Высокая 12А)\n\n"
        output += "Кешбек = {:.0f} внутренними рублями\n (через 2 недели, если закажете самостоятельно на сайте)".format(cashback_amount)

        # Вывод пользователю
        bot.send_message(chat_id=message.chat.id, text=output)
        # send_debug_message("Калькулятор ОК")
    except ValueError:
        bot.send_message(chat_id=message.chat.id, text="Сломался калькулятор, что-то пошло не так (Только цифры)")
        # send_debug_message("Калькулятор Ошибка")