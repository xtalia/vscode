console.log('ms_show_all.js loaded');

// Function to show all blocks with class="tab-content"
function showAllTabContents() {
    const hiddenElements = document.querySelectorAll('.tab-content .hidden');
    hiddenElements.forEach(element => {
        element.classList.remove('hidden');
    });
}

// Create button
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

// Run the function to create the button after the page is fully loaded
window.addEventListener('load', () => {
    setTimeout(createButton, 3000); // 3-second delay before creating the button
});
