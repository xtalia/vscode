// ms_show_all.js

// Function to show all blocks with class="tab-content"
function showAllTabContent() {
    const tabContents = document.querySelectorAll('.tab-content');
    tabContents.forEach(tabContent => {
        tabContent.style.display = 'block';
    });
}

// Run the function after the page is fully loaded
window.addEventListener('load', showAllTabContent);
