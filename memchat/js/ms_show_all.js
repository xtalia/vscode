// ==UserScript==
// @name         Show All Tab Contents Button
// @namespace    http://tampermonkey.net/
// @version      1.2
// @description  Добавляет кнопку для показа всех блоков с class="tab-content", убирая у них класс "hidden"
// @author       Your Name
// @match        https://online.moysklad.ru/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Функция для показа всех блоков с class="tab-content"
    function showAllTabContents() {
        const hiddenElements = document.querySelectorAll('.tab-content .hidden');
        hiddenElements.forEach(element => {
            element.classList.remove('hidden');
        });
    }

    // Создание кнопки
    function createButton() {
        const button = document.createElement('button');
        button.innerText = 'Show All Tab Contents';
        button.style.position = 'fixed';
        button.style.top = '10px';
        button.style.right = '10px';
        button.style.zIndex = '1000';
        button.style.padding = '10px';
        button.style.backgroundColor = '#007bff';
        button.style.color = '#fff';
        button.style.border = 'none';
        button.style.borderRadius = '5px';
        button.style.cursor = 'pointer';

        button.addEventListener('click', showAllTabContents);

        document.body.appendChild(button);
    }

    // Запуск функции создания кнопки после полной загрузки страницы
    window.addEventListener('load', () => {
        setTimeout(createButton, 3000); // Задержка в 3 секунды перед созданием кнопки
    });
})();
