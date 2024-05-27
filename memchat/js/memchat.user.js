// ==UserScript==
// @name         Мемный чат
// @namespace    http://tampermonkey.net/
// @version      1.4
// @description  Набор скриптов
// @match        https://online.moysklad.ru/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';

    console.log('Main userscript loaded');

    const scriptsToLoad = [
        'https://raw.githubusercontent.com/xtalia/vscode/main/memchat/js/ms_show_all.js',
        'https://raw.githubusercontent.com/xtalia/vscode/main/memchat/js/price_calculator.js'
    ];

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
})();
