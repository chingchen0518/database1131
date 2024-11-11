document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('search');
    const dropdown = document.querySelector('.dropdown');
    const dropdownContent = document.querySelector('.dropdown-content');
    const dropdownItems = dropdownContent.querySelectorAll('.dropdown-item');

    // Toggle dropdown visibility
    searchInput.addEventListener('focus', function() {
        dropdown.classList.add('show');
    });

    // Close dropdown if click outside
    document.addEventListener('click', function(event) {
        if (!dropdown.contains(event.target)) {
            dropdown.classList.remove('show');
        }
    });

    // Filter dropdown items
    searchInput.addEventListener('input', function() {
        const filter = searchInput.value.toLowerCase();
        dropdownItems.forEach(item => {
            const text = item.textContent.toLowerCase();
            item.style.display = text.includes(filter) ? 'block' : 'none';
        });
    });

    // Select item
    dropdownContent.addEventListener('click', function(event) {
        if (event.target.classList.contains('dropdown-item')) {
            searchInput.value = event.target.textContent;
            dropdown.classList.remove('show');
        }
    });
});
