// ==UserScript==
// @name         Мемный чат
// @namespace    http://tampermonkey.net/
// @version      1.6.4
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
        'https://raw.githubusercontent.com/xtalia/vscode/main/memchat/js/price_calculator.js',
        'https://raw.githubusercontent.com/xtalia/vscode/main/memchat/js/links.user.js'
    ];

    function loadScript(url) {
        return new Promise((resolve, reject) => {
            GM_xmlhttpRequest({
                method: 'GET',
                url: url,
                onload: function(response) {
                    console.log(`Loaded script from ${url}`);
                    const script = document.createElement('script');
                    script.textContent = response.responseText;
                    document.body.appendChild(script);
                    resolve();
                },
                onerror: function(error) {
                    console.error(`Failed to load script from ${url}`, error);
                    reject(error);
                }
            });
        });
    }

    async function loadAllScripts() {
        try {
            await Promise.all(scriptsToLoad.map(loadScript));
            console.log('All scripts loaded successfully');
        } catch (error) {
            console.error('Error loading scripts:', error);
        }
    }

    function showAllTabContents() {
        const hiddenElements = document.querySelectorAll('.tab-content .hidden');
        hiddenElements.forEach(element => {
            element.classList.remove('hidden');
        });
    }

    function addCustomStyles() {
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
    }

    function registerMenuCommands() {
        GM_registerMenuCommand('Раскрыть всю карточку товара', showAllTabContents, 'S');
        GM_registerMenuCommand('Обновить скрипты мемные', function() {
            console.log('Reloading memchat scripts...');
            loadAllScripts();
        });
    }

    function initialize() {
        addCustomStyles();
        registerMenuCommands();
        loadAllScripts();
        });
    }

    // Call the initialize function to set up the script
    initialize();

    // Placeholder for additional functions
    // Add new functions below this line

})();
