// ==UserScript==
// @name         Script Loader with Settings Panel
// @namespace    http://tampermonkey.net/
// @version      1.5
// @description  Load scripts based on user settings
// @match        https://online.moysklad.ru/*
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Function to load a script
    function loadScript(url) {
        const script = document.createElement('script');
        script.src = url;
        script.async = true;
        document.body.appendChild(script);
    }

    // URLs of the scripts to load
    const scripts = {
        'ms_show_all': 'https://raw.githubusercontent.com/xtalia/vscode/main/memchat/js/ms_show_all.js',
        'price_calculator': 'https://raw.githubusercontent.com/xtalia/vscode/main/memchat/js/price_calculator.js'
    };

    // Load scripts based on user preferences
    Object.keys(scripts).forEach(key => {
        if (localStorage.getItem(key) === 'true') {
            loadScript(scripts[key]);
        }
    });

    // Function to create the settings panel
    function createSettingsPanel() {
        const panel = document.createElement('div');
        panel.style.position = 'fixed';
        panel.style.top = '10px';
        panel.style.left = '10px';
        panel.style.width = '200px';
        panel.style.backgroundColor = '#fff';
        panel.style.border = '1px solid #ccc';
        panel.style.padding = '10px';
        panel.style.zIndex = '10000';
        panel.style.display = 'none';
        panel.id = 'settings-panel';

        const title = document.createElement('h3');
        title.innerText = 'Script Settings';
        panel.appendChild(title);

        Object.keys(scripts).forEach(key => {
            const label = document.createElement('label');
            label.style.display = 'block';
            label.style.marginBottom = '10px';

            const checkbox = document.createElement('input');
            checkbox.type = 'checkbox';
            checkbox.id = key;
            checkbox.checked = localStorage.getItem(key) === 'true';
            checkbox.addEventListener('change', () => {
                localStorage.setItem(key, checkbox.checked);
            });

            label.appendChild(checkbox);
            label.appendChild(document.createTextNode(` ${key}`));
            panel.appendChild(label);
        });

        document.body.appendChild(panel);
    }

    // Toggle the settings panel visibility
    function toggleSettingsPanel() {
        const panel = document.getElementById('settings-panel');
        if (panel.style.display === 'none') {
            panel.style.display = 'block';
        } else {
            panel.style.display = 'none';
        }
    }

    // Create the settings panel on page load
    window.addEventListener('load', createSettingsPanel);

    // Add event listener for toggling the settings panel with Ctrl+M
    document.addEventListener('keydown', (event) => {
        if (event.ctrlKey && event.key === 'm') {
            toggleSettingsPanel();
        }
    });
})();
