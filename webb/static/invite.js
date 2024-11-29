document.addEventListener('DOMContentLoaded', function() {
    const modalOverlay = document.getElementById('modalOverlay');
    const inviteMembersLink = document.getElementById('inviteMembersLink');
    const modalInviteBtn = document.querySelector('.modal-invite-btn');
    const successMessage = document.getElementById('successMessage');

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
        modalInviteBtn.addEventListener('click', function() {
            addNewRow(this);
        });
    });

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

     // Handle invite button click
     modalInviteBtn.addEventListener('click', function() {
        const name = document.getElementById('memberName').value.trim();
        const email = document.getElementById('memberEmail').value.trim();
        const phone = document.getElementById('memberPhone').value.trim();
        const role = document.getElementById('workspaceRole').value;

        let isValid = true;

        // Validasi input
        if (!name || !email || !phone || !role) {
            alert('Please fill all fields');
            isValid = false;
        }

        if (isValid) {
            // Ambil data dari localStorage atau buat array baru
            const members = JSON.parse(localStorage.getItem('members')) || [];

            // Cek apakah data sudah ada
            const isDuplicate = members.some(member => member.name === name && member.email === email && member.phone === phone);

            if (isDuplicate) {
                alert('This member is already added!');
                return;
            }

            // Tambahkan data baru ke array
            members.push({ name, email, phone, role });

            // Simpan kembali ke localStorage
            localStorage.setItem('members', JSON.stringify(members));

            alert('Member added successfully!');
            resetForm();
        }
    });

    // Function to show success message
    function showSuccessMessage() {
        successMessage.style.display = 'block';
        setTimeout(() => {
            successMessage.style.display = 'none';
        }, 3000);
    };

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
    };
});