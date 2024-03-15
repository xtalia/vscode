import streamlit as st

cash = float()



def process_cash_amount(message, bot):
    try:
        # send_debug_message(f"{message.from_user.id} запросил Калькулятор")
        cash = float(message.text.strip())
        
        qr_price = round(cash * 1.01501, -2) -10
        card_price = round(cash * 1.0301, -2) -10
        rassrochka_price_six = round(cash * 1.0701, -2) -10
        rassrochka_price_ten = round(cash * 1.101, -2) -10
        credit_price = round(cash * 1.1801, -2) -10
        cashback_amount = round(cash * 0.01)
        
        credit_month = 36
        twenty = round(credit_price * ((20/12/100) * (1 + (20/12/100)) ** credit_month) / ((1 + (20/12/100)) ** credit_month - 1), 0)
        fourty = round(credit_price * ((40/12/100) * (1 + (40/12/100)) ** credit_month) / ((1 + (40/12/100)) ** credit_month - 1), 0)

        # Оформление сообщения
        output = "💵 Стоимость: {:.0f} рублей с учетом скидки за оплату наличными\n\n".format(cash)
        output += "📷 QR = {:.0f} рублей\n".format(qr_price)
        output += "💳 по карте = {:.0f} рублей\n\n".format(card_price)
        output += "️🏦 в рассрочку\n"
        output += "️🔹 ОТП = {:.0f} рублей (от {:.0f} руб. на 6 месяцев)\n".format(rassrochka_price_six, rassrochka_price_six / 6)
        output += "🔹 Другие банки = {:.0f} рублей (от {:.0f} руб. на 10 месяцев)\n".format(rassrochka_price_ten, rassrochka_price_ten / 10)
        output += "🏛 в кредит = {:.0f} рублей + % Банка".format(credit_price)
        # 20% годовых на 36 мес = 60% | 40 годовых на 36 = 120%
        output += "(от {:.0f} - {:.0f} руб. сроком до 36 месяцев)\n".format(twenty, fourty)
        output += "** %Банка ~ от 20 до 40% годовых (точные условия может предоставить только менеджер)\n\n"
        output += "💸 Кешбек = {:.0f} внутренними рублями\n (через 2 недели, если закажете самостоятельно на сайте)".format(cashback_amount)

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



def cash_amount():
    st.subheader("Калькулятор карты, кредита, кешбека")
    try:
        # Запрашиваем сумму наличными
        cash = float(st.text_input("Введите сумму наличными:", value=228))
        credit_month = int(st.slider("Срок кредитования", 1,36,value=36))
        # Расчет по карте, рассрочку, кредиту, кешбеку
        # qr_price = round(cash * 1.015, -2)  - 10
        qr_price = round(cash * 1.01501, -2) -10
        card_price = round(cash * 1.0301, -2) -10
        rassrochka_price_six = round(cash * 1.0701, -2) -10
        rassrochka_price_ten = round(cash * 1.101, -2) -10
        
        credit_price = round(cash * 1.1801, -2) -10
        cashback_amount = round(cash * 0.01)


        twenty = round(credit_price * ((20/12/100) * (1 + (20/12/100)) ** credit_month) / ((1 + (20/12/100)) ** credit_month - 1), 0)
        fourty = round(credit_price * ((40/12/100) * (1 + (40/12/100)) ** credit_month) / ((1 + (40/12/100)) ** credit_month - 1), 0)

        

        # Оформление сообщения
        output = "💵 Стоимость: {:.0f} рублей с учетом скидки за оплату наличными  \n".format(cash)
        output += "📷 QR = {:.0f} рублей  \n".format(qr_price)
        output += "💳 по карте = {:.0f} рублей  \n".format(card_price)
        output += "️🏦 в рассрочку  \n"
        output += "️🔹 ОТП = {:.0f} рублей (от {:.0f} руб. на 6 месяцев)  \n".format(rassrochka_price_six, rassrochka_price_six / 6)
        output += "🔹 Другие банки = {:.0f} рублей (от {:.0f} руб. на 10 месяцев)  \n".format(rassrochka_price_ten, rassrochka_price_ten / 10)
        output += "🏛 в кредит = {:.0f} рублей + % Банка".format(credit_price)
        output += (f"(от {int(twenty)} - {int(fourty)} руб. сроком на {int(credit_month)} мес)  \n")
        output += "** %Банка ~ от 20 до 40% годовых** (точные условия может предоставить только менеджер)  \n"
        output += "💸 Кешбек = {:.0f} внутренними рублями  \n (через 2 недели, если закажете самостоятельно на сайте)".format(cashback_amount)

        # Вывод пользователю
        st.write(output)
    except ValueError:
        st.write("Сломался калькулятор, что-то пошло не так (Только цифры)")
     
def original_price():
    st.subheader("Калькулятор скидки для мс")
    try:
        # Запрашиваем изначальную цену
        original_price = float(st.text_input("Введите изначальную цену:", value=228))
        discount = float(st.text_input("Введите сумму скидки:", value=228))
        st.button("Посчитать")
            
        discounted_price = original_price - discount
        discount_percentage = 100 - discounted_price / (original_price * 0.01)
        result_message = f"Изначальная цена: {int(original_price)}  \n"
        result_message += f"Скидка: {discount}  \n"
        result_message += f"Процент скидки: {discount_percentage}  \n"
        result_message += f"Сумма со скидкой: {discounted_price}"

        # Отправляем результат пользователю
        st.write(result_message)
    except:
        st.write("Сломался калькулятор, что-то пошло не так (Только цифры)")
        