document.addEventListener('DOMContentLoaded', function() {
    const groupProjectView = document.getElementById('groupProjectView');
    const groupProjectLink = document.getElementById('groupProjectLink');

    function showView(viewToShow) {
        groupProjectView.style.display = 'none';
        viewToShow.style.display = 'block';
    }

    groupProjectLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(groupProjectView);
    });

    // Add row functionality for tables
    window.addRow = function(tableId) {
        const table = document.getElementById(tableId);
        const tbody = table.querySelector('tbody');
        const firstRow = tbody.querySelector('tr');
        const newRow = firstRow.cloneNode(true);
        
        // Clear input values in the new row
        newRow.querySelectorAll('input').forEach(input => {
            input.value = '';
        });
        
        tbody.appendChild(newRow);
    };

    function addRow(tableId) {
        const table = document.getElementById(tableId);
        const tbody = table.querySelector('tbody');
        const firstRow = tbody.querySelector('tr');
        const newRow = firstRow.cloneNode(true);
        
        // Clear input values in the new row
        newRow.querySelectorAll('input').forEach(input => {
            input.value = '';
        });
        
        tbody.appendChild(newRow);
    }

    function addNewRow(button) {
        const previousRow = button.previousElementSibling;
        const newRow = previousRow.cloneNode(true);
        
        // Clear semua input dalam row baru
        newRow.querySelectorAll('input').forEach(input => {
            input.value = '';
        });
        
        // Insert row baru sebelum tombol
        button.parentNode.insertBefore(newRow, button);
    }
})