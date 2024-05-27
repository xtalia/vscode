// price_calculator.js

function createCalculator() {
    const container = document.createElement('div');
    container.style.position = 'fixed';
    container.style.bottom = '10px';
    container.style.right = '10px';
    container.style.width = '300px';
    container.style.backgroundColor = '#f9f9f9';
    container.style.border = '1px solid #ccc';
    container.style.borderRadius = '5px';
    container.style.boxShadow = '0 0 10px rgba(0, 0, 0, 0.1)';
    container.style.padding = '10px';
    container.style.zIndex = '1000';

    const header = document.createElement('div');
    header.style.display = 'flex';
    header.style.justifyContent = 'space-between';
    header.style.alignItems = 'center';

    const title = document.createElement('span');
    title.innerText = 'Calculator';
    header.appendChild(title);

    const toggleButton = document.createElement('button');
    toggleButton.innerText = '-';
    toggleButton.style.backgroundColor = 'transparent';
    toggleButton.style.border = 'none';
    toggleButton.style.cursor = 'pointer';
    toggleButton.addEventListener('click', () => {
        if (content.style.display === 'none') {
            content.style.display = 'block';
            toggleButton.innerText = '-';
        } else {
            content.style.display = 'none';
            toggleButton.innerText = '+';
        }
    });
    header.appendChild(toggleButton);

    container.appendChild(header);

    const content = document.createElement('div');

    const cashInput = document.createElement('input');
    cashInput.type = 'number';
    cashInput.placeholder = 'Enter cash amount';
    cashInput.style.width = '100%';
    cashInput.style.marginBottom = '10px';
    content.appendChild(cashInput);

    const modeSelect = document.createElement('select');
    const optionAll = document.createElement('option');
    optionAll.value = 'all';
    optionAll.innerText = 'Для всех';
    modeSelect.appendChild(optionAll);
    const optionBalakovo = document.createElement('option');
    optionBalakovo.value = 'balakovo';
    optionBalakovo.innerText = 'Для Балаково';
    modeSelect.appendChild(optionBalakovo);
    modeSelect.style.width = '100%';
    modeSelect.style.marginBottom = '10px';
    content.appendChild(modeSelect);

    const calculateButton = document.createElement('button');
    calculateButton.innerText = 'Посчитать';
    calculateButton.style.width = '100%';
    calculateButton.style.marginBottom = '10px';
    content.appendChild(calculateButton);

    const resultField = document.createElement('textarea');
    resultField.style.width = '100%';
    resultField.style.height = '100px';
    resultField.style.marginBottom = '10px';
    resultField.readOnly = true;
    content.appendChild(resultField);

    calculateButton.addEventListener('click', () => {
        const cash = parseFloat(cashInput.value);
        const mode = modeSelect.value;
        let qr_price, card_price, rassrochka_price_six, rassrochka_price_ten, credit_price, cashback_amount;
        let credit_month = 36;
        let twenty = Math.round(credit_price * ((20/12/100) * (1 + (20/12/100)) ** credit_month) / ((1 + (20/12/100)) ** credit_month - 1), 0);
        let fourty = Math.round(credit_price * ((40/12/100) * (1 + (40/12/100)) ** credit_month) / ((1 + (40/12/100)) ** credit_month - 1), 0);

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

        resultField.value = `
Стоимость: ${cash} рублей с учетом скидки за оплату наличными
QR = ${qr_price} рублей
по карте = ${card_price} рублей

в рассрочку
ОТП = ${rassrochka_price_six} рублей (от ${Math.round(rassrochka_price_six / 6)} руб. на 6 месяцев)
Другие банки = ${rassrochka_price_ten} рублей (от ${Math.round(rassrochka_price_ten / 10)} руб. на 10 месяцев)

в кредит = ${credit_price} + процент Банка
от ${twenty} - ${fourty} руб. сроком до ${credit_month} месяцев)
** %Банка ~ от 20 до 40% годовых (точные условия может предоставить только менеджер)
Кешбек = ${cashback_amount} внутренними баллами
        `;
    });

    container.appendChild(content);
    document.body.appendChild(container);
}

window.addEventListener('load', createCalculator);
