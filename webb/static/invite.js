document.addEventListener('DOMContentLoaded', function() {
    const modalOverlay = document.getElementById('modalOverlay');
    const inviteMembersLink = document.getElementById('inviteMembersLink');
    const modalInviteBtn = document.querySelector('.modal-invite-btn');
    const successMessage = document.getElementById('successMessage');
    const groupProjectTable = document.querySelector('#groupProjectView table');

    function openModal() {
        const modalOverlay = document.getElementById('modalOverlay');
        modalOverlay.classList.add('active');
    }

    // Open modal
    inviteMembersLink.addEventListener('click', function(e) {
        e.preventDefault();
        modalOverlay.classList.add('active');
    });

    // Close modal when clicking outside
    modalOverlay.addEventListener('click', function(e) {
        if (e.target === modalOverlay) {
            modalOverlay.classList.remove('active');
            resetForm();
        }
    });

    // Close modal when pressing Escape key
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && modalOverlay.classList.contains('active')) {
            modalOverlay.classList.remove('active');
            resetForm();
        }
    });

    // Event listener untuk tombol Add
    document.querySelectorAll('.add-btn').forEach(button => {
        button.addEventListener('click', function() {
            addNewRow(this);
        });
    });

    // Function to validate email
    function isValidEmail(email) {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    // Function to validate phone number
    function isValidPhone(phone) {
        return /^\+?[\d\s-]{10,}$/.test(phone);
    }

    // Function to show error
    function showError(inputId, errorId, show) {
        const input = document.getElementById(inputId);
        const error = document.getElementById(errorId);
        if (show) {
            input.classList.add('input-error');
            error.style.display = 'block';
        } else {
            input.classList.remove('input-error');
            error.style.display = 'none';
        }
    }

    // Function to add member to table
    function addMemberToTable(name, email, phone) {
        const newRow = groupProjectTable.insertRow(-1);
        
        const nameCell = newRow.insertCell(0);
        const emailCell = newRow.insertCell(1);
        const phoneCell = newRow.insertCell(2);

        nameCell.textContent = name;
        emailCell.textContent = email;
        phoneCell.textContent = phone;
    }

    // Function to show success message
    function showSuccessMessage() {
        successMessage.style.display = 'block';
        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 3000);
    }

    // Reset form function
    function resetForm() {
        document.getElementById('memberName').value = '';
        document.getElementById('memberEmail').value = '';
        document.getElementById('memberPhone').value = '';
        document.getElementById('workspaceRole').value = '';
        
        // Reset all errors
        showError('memberName', 'nameError', false);
        showError('memberEmail', 'emailError', false);
        showError('memberPhone', 'phoneError', false);
    }

    // Handle invite button click
    modalInviteBtn.addEventListener('click', function() {
        console.log('Invite Clicked')
        const name = document.getElementById('memberName').value.trim();
        const email = document.getElementById('memberEmail').value.trim();
        const phone = document.getElementById('memberPhone').value.trim();
        const role = document.getElementById('workspaceRole').value;

        let isValid = true;

        // Validate name
        if (!name) {
            showError('memberName', 'nameError', true);
            isValid = false;
        } else {
            showError('memberName', 'nameError', false);
        }

        // Validate email
        if (!email || !isValidEmail(email)) {
            showError('memberEmail', 'emailError', true);
            isValid = false;
        } else {
            showError('memberEmail', 'emailError', false);
        }

        // Validate phone
        if (!phone || !isValidPhone(phone)) {
            showError('memberPhone', 'phoneError', true);
            isValid = false;
        } else {
            showError('memberPhone', 'phoneError', false);
        }

        if (!role) {
            alert('Please select a role');
            isValid = false;
        }

        if (isValid) {
            // Add member to table
            addMemberToTable(name, email, phone);
            
            // Show success message
            showSuccessMessage();
            
            // Close modal and reset form
        modalOverlay.classList.remove('active');
        resetForm();
        }
    });
})