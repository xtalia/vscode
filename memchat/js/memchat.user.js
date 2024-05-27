// ==UserScript==
// @name         Мемный чат 4
// @namespace    http://tampermonkey.net/
// @version      1.6
// @description  Набор скриптов
// @match        https://online.moysklad.ru/*
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// @grant        GM_addStyle
// ==/UserScript==

(function() {
    'use strict';

    console.log('Main userscript loaded');

    const scriptsToLoad = [
        'https://raw.githubusercontent.com/xtalia/vscode/main/memchat/js/price_calculator.js'
    ];

    function loadScripts() {
        scriptsToLoad.forEach(url => {
            GM_xmlhttpRequest({
                method: 'GET',
                url: url,
                onload: function(response) {
                    console.log(`Loaded script from ${url}`);
                    const script = document.createElement('script');
                    script.textContent = response.responseText;
                    document.body.appendChild(script);
                },
                onerror: function(error) {
                    console.error(`Failed to load script from ${url}`, error);
                }
            });
        });
    }

    // Функция для показа всех блоков с class="tab-content"
    function showAllTabContents() {
        const hiddenElements = document.querySelectorAll('.tab-content .hidden');
        hiddenElements.forEach(element => {
            element.classList.remove('hidden');
        });
    }

    // Добавление стилей для контекстного меню
    GM_addStyle(`
        .gm-context-menu {
            z-index: 1000;
            position: fixed;
            top: 10px;
            right: 10px;
            background-color: #f9f9f9;
            border: 1px solid #ccc;
            border-radius: 5px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            padding: 10px;
            cursor: pointer;
        }
    `);

    // Регистрация пункта в контекстном меню
    GM_registerMenuCommand('Show All Tab Contents', showAllTabContents, 'S');

    // Функция для создания контекстного меню
    function createContextMenu() {
        const contextMenu = document.createElement('div');
        contextMenu.classList.add('gm-context-menu');
        contextMenu.textContent = 'Show All Tab Contents';
        contextMenu.addEventListener('click', showAllTabContents);
        document.body.appendChild(contextMenu);
    }

    // Запуск функции создания контекстного меню после полной загрузки страницы
    window.addEventListener('load', () => {
        setTimeout(createContextMenu, 3000); // Задержка в 3 секунды перед созданием контекстного меню
    });

    // Register menu command to reload scripts
    GM_registerMenuCommand('Обновить скрипты мемные', function() {
        console.log('Reloading memchat scripts...');
        loadScripts();
    });

    // Initial load of scripts
    loadScripts();

})();
