// ==UserScript==
// @name         Мемный чат
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Набор скриптов
// @match        https://online.moysklad.ru/*
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// ==/UserScript==

(function() {
    'use strict';

    const scriptsToLoad = [
        'https://github.com/xtalia/vscode/raw/main/memchat/js/price_calculator.js',
        'https://github.com/xtalia/vscode/raw/main/memchat/js/ms_show_all.js'
    ];

    scriptsToLoad.forEach(url => {
        GM_xmlhttpRequest({
            method: 'GET',
            url: url,
            onload: function(response) {
                const script = document.createElement('script');
                script.textContent = response.responseText;
                document.head.appendChild(script);
            }
        });
    });
})();
