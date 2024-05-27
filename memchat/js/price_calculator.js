// ==UserScript==
// @name         Price Calculator
// @namespace    https://github.com/xtalia/vscode/blob/main/memchat/js/price_calculator.js
// @version      1.5.1
// @description  Добавляет окошко для расчета цен с возможностью сворачивания и вывода результатов в текстовое поле, а также с функцией для расчета скидки
// @author       Serg
// @match        https://online.moysklad.ru/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    function createCalculator() {
        const container = document.createElement('div');
        container.style.cssText = 'position: fixed; bottom: 10px; right: 10px; width: 300px; background-color: #f9f9f9; border: 1px solid #ccc; border-radius: 5px; box-shadow: 0 0 10px rgba(0, 0, 0, 0.1); padding: 10px; z-index: 1000;';

        const header = document.createElement('div');
        header.style.cssText = 'display: flex; justify-content: space-between; align-items: center;';

        const title = document.createElement('span');
        title.textContent = 'Калькулятор 1.5.1';
        header.appendChild(title);

        const toggleButton = document.createElement('button');
        toggleButton.textContent = '-';
        toggleButton.style.cssText = 'background-color: transparent; border: none; cursor: pointer;';
        toggleButton.addEventListener('click', () => {
            content.style.display = content.style.display === 'none' ? 'block' : 'none';
            toggleButton.textContent = content.style.display === 'none' ? '+' : '-';
        });
        header.appendChild(toggleButton);

        container.appendChild(header);

        const content = document.createElement('div');
        content.style.display = 'block';

        const cashInput = createInputElement('number', 'Введите сумму');
        content.appendChild(cashInput);

        const modeSelect = createSelectElement([
            { value: 'all', text: 'Для всех' },
            { value: 'balakovo', text: 'Для Балаково' }
        ]);
        content.appendChild(modeSelect);

        const calculateButton = createButtonElement('Посчитать', () => calculate());
        content.appendChild(calculateButton);

        const resultField = createTextAreaElement('', 100);
        content.appendChild(resultField);

        const discountInput = createInputElement('number', 'Введите сумму скидки');
        content.appendChild(discountInput);

        const applyDiscountButton = createButtonElement('Применить скидку', () => applyDiscount());
        content.appendChild(applyDiscountButton);

        function calculate() {
            const cash = parseFloat(cashInput.value);
            const mode = modeSelect.value;
            let qr_price, card_price, rassrochka_price_six, rassrochka_price_ten, credit_price, cashback_amount;
            let credit_month = 36;

            if (mode === 'all') {
                qr_price = Math.round(cash * 1.0401 / 100) * 100 - 10;
                card_price = Math.round(cash * 1.0501 / 100) * 100 - 10;
                rassrochka_price_six = Math.round(cash * 1.1001 / 100) * 100 - 10;
                rassrochka_price_ten = Math.round(cash * 1.1301 / 100) * 100 - 10;
                credit_price = Math.round(cash * 1.2001 / 100) * 100 - 10;
                cashback_amount = Math.round(cash * 0.01);
            } else if (mode === 'balakovo') {
                qr_price = Math.round(cash * 1.01501 / 100) * 100 - 10;
                card_price = Math.round(cash * 1.0301 / 100) * 100 - 10;
                rassrochka_price_six = Math.round(cash * 1.0701 / 100) * 100 - 10;
                rassrochka_price_ten = Math.round(cash * 1.1001 / 100) * 100 - 10;
                credit_price = Math.round(cash * 1.1801 / 100) * 100 - 10;
                cashback_amount = Math.round(cash * 0.01);
            }

            const twenty = Math.round(credit_price * ((20 / 12 / 100) * (1 + (20 / 12 / 100)) ** credit_month) / (((1 + (20 / 12 / 100)) ** credit_month) - 1));
            const forty = Math.round(credit_price * ((40 / 12 / 100) * (1 + (40 / 12 / 100)) ** credit_month) / (((1 + (40 / 12 / 100)) ** credit_month) - 1));

            resultField.value = `
💵 Стоимость: ${cash} рублей с учетом скидки за оплату наличными
📷 QR = ${qr_price} рублей
💳 по карте = ${card_price} рублей

️🏦 в рассрочку
️🔹 ОТП = ${rassrochka_price_six} рублей (от ${Math.round(rassrochka_price_six / 6)} руб. на 6 месяцев)
🔹 Другие банки = ${rassrochka_price_ten} рублей (от ${Math.round(rassrochka_price_ten / 10)} руб. на 10 месяцев)

🏛 в кредит = ${credit_price} + процент Банка
от ${twenty} - ${forty} руб. сроком до ${credit_month} месяцев)
** %Банка ~ от 20 до 40% годовых (точные условия может предоставить только менеджер)
💸 Кешбек = ${cashback_amount} внутренними баллами
`.trim();
        }

        function applyDiscount() {
            const originalPrice = parseFloat(cashInput.value);
            const discount = parseFloat(discountInput.value);
            
            if (!isNaN(discount)) {
                const discountedPrice = originalPrice - discount;
                const discountPercentage = 100 - (discountedPrice / (originalPrice * 0.01));

    resultField.value = `
🎉 Применена скидка:
🔹 Изначальная цена: ${originalPrice} рублей
🔹 Скидка: ${discount} рублей
🔹 Процент скидки: ${discountPercentage} %
🔹 Сумма со скидкой: ${discountedPrice} рублей
    `.trim();

            } else {
                resultField.value = 'Ошибка: Введите корректную сумму скидки (только цифры).';
            }
        }

        function createInputElement(type, placeholder) {
            const input = document.createElement('input');
            input.type = type;
            input.placeholder = placeholder;
            input.style.width = '100%';
            input.style.marginBottom = '10px';
            return input;
        }

        function createSelectElement(options) {
            const select = document.createElement('select');
            select.style.width = '100%';
            select.style.marginBottom = '10px';
            options.forEach(option => {
                const opt = document.createElement('option');
                opt.value = option.value;
                opt.textContent = option.text;
                select.appendChild(opt);
            });
            return select;
        }

        function createButtonElement(text, clickHandler) {
            const button = document.createElement('button');
            button.textContent = text;
            button.style.width = '100%';
            button.style.marginBottom = '10px';
            button.style.cursor = 'pointer';
            button.addEventListener('click', clickHandler);
            return button;
        }

        function createTextAreaElement(value, height) {
            const textarea = document.createElement('textarea');
            textarea.value = value;
            textarea.style.width = '100%';
            textarea.style.height = height + 'px';
            textarea.style.marginBottom = '10px';
            textarea.readOnly = true;
            return textarea;
        }

        container.appendChild(content);
        document.body.appendChild(container);
    }

    window.addEventListener('load', createCalculator);
})();
