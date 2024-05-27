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
        url: 'https://example.com/external-script.js',
        onload: function(response) {
            const script = document.createElement('script');
            script.textContent = response.responseText;
            document.head.appendChild(script);
        }
    });
    GM_xmlhttpRequest({
        method: 'GET',
        url: 'https://example.com/external-script.js',
        onload: function(response) {
            const script = document.createElement('script');
            script.textContent = response.responseText;
            document.head.appendChild(script);
        }
    });

})();