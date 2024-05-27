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

    GM_xmlhttpRequest({
        method: 'GET',
        url: 'https://github.com/xtalia/vscode/raw/main/memchat/js/ms_show_all.js',
        onload: function(response) {
            const script = document.createElement('script');
            script.textContent = response.responseText;
            document.head.appendChild(script);
        }
    });
    GM_xmlhttpRequest({
        method: 'GET',
        url: 'https://github.com/xtalia/vscode/raw/main/memchat/js/price_calculator.js',
        onload: function(response) {
            const script = document.createElement('script');
            script.textContent = response.responseText;
            document.head.appendChild(script);
        }
    });

})();