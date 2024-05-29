// ==UserScript==
// @name         Мемный чат
// @namespace    http://tampermonkey.net/
// @version      1.6.6
// @description  Набор скриптов
// @match        https://online.moysklad.ru/*
// @grant        GM_xmlhttpRequest
// @grant        GM_registerMenuCommand
// ==/UserScript==

(function() {
    'use strict';

    console.log('Main userscript loaded');

    function showAllTabContents() {
        const hiddenElements = document.querySelectorAll('.tab-content .hidden');
        hiddenElements.forEach(element => {
            element.classList.remove('hidden');
        });
    }

    function registerMenuCommands() {
        GM_registerMenuCommand('Раскрыть всю карточку товара', showAllTabContents, 'S');
    }

    function initialize() {
        registerMenuCommands();
        console.log('Initialization complete');
    }

    // Call the initialize function to set up the script
    initialize();

    // Placeholder for additional functions
    // Add new functions below this line

})();
