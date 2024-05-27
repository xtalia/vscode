// ==UserScript==
// @name         Полезные ссылки
// @namespace    http://tampermonkey.net/
// @version      1.0
// @description  Выдвижная панель с полезными ссылками и кнопкой для обновления списка ссылок
// @author       Serg
// @match        https://online.moysklad.ru/*
// @grant        GM_xmlhttpRequest
// @grant        GM_addStyle
// ==/UserScript==

(function() {
    'use strict';

    const panelWidth = 10; // Ширина выдвижной панели в пикселях

    const panel = document.createElement('div');
    panel.id = 'usefulLinksPanel';
    panel.style.cssText = `
        position: fixed;
        top: 50%;
        right: 0;
        transform: translateY(-50%);
        width: ${panelWidth}px;
        background-color: #fff;
        border-left: 1px solid #ccc;
        box-shadow: -1px 0 10px rgba(0, 0, 0, 0.1);
        z-index: 1000;
        transition: width 0.3s ease;
        overflow: hidden;
    `;

    const closeButton = document.createElement('button');
    closeButton.textContent = '❌';
    closeButton.style.cssText = `
        position: absolute;
        top: 5px;
        right: 5px;
        background-color: transparent;
        border: none;
        cursor: pointer;
    `;
    closeButton.addEventListener('click', () => {
        panel.style.width = '0';
    });
    panel.appendChild(closeButton);

    const linksContainer = document.createElement('div');
    panel.appendChild(linksContainer);

    const refreshButton = document.createElement('button');
    refreshButton.textContent = 'Обновить ссылки';
    refreshButton.style.cssText = `
        width: 100%;
        padding: 10px;
        background-color: #007bff;
        color: #fff;
        border: none;
        cursor: pointer;
    `;
    refreshButton.addEventListener('click', () => {
        updateLinks();
    });
    panel.appendChild(refreshButton);

    function updateLinks() {
        GM_xmlhttpRequest({
            method: 'GET',
            url: 'https://raw.githubusercontent.com/xtalia/vscode/main/memchat/js/links.json',
            onload: function(response) {
                try {
                    const linksData = JSON.parse(response.responseText);
                    renderLinks(linksData);
                } catch (error) {
                    console.error('Failed to parse links JSON', error);
                }
            },
            onerror: function(error) {
                console.error('Failed to load links JSON', error);
            }
        });
    }

    function renderLinks(linksData) {
        linksContainer.innerHTML = '';
        linksData.forEach(link => {
            const linkElement = document.createElement('a');
            linkElement.href = link.url;
            linkElement.textContent = link.name;
            linkElement.style.cssText = `
                display: block;
                padding: 10px;
                color: #333;
                text-decoration: none;
                border-bottom: 1px solid #eee;
                transition: background-color 0.3s ease;
            `;
            linkElement.addEventListener('mouseover', () => {
                linkElement.style.backgroundColor = '#f0f0f0';
            });
            linkElement.addEventListener('mouseout', () => {
                linkElement.style.backgroundColor = 'transparent';
            });
            linksContainer.appendChild(linkElement);
        });
    }

    // Initial load of links
    updateLinks();

    // Add panel to the document
    document.body.appendChild(panel);

    // Hover to expand panel
    panel.addEventListener('mouseenter', () => {
        panel.style.width = '250px'; // Установите здесь нужную ширину панели при наведении
    });

    panel.addEventListener('mouseleave', () => {
        panel.style.width = `${panelWidth}px`;
    });

    // Add styles
    GM_addStyle(`
        #usefulLinksPanel a:hover {
            background-color: #f0f0f0;
        }
    `);

})();
