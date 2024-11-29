document.addEventListener('DOMContentLoaded', function() {
    const groupProjectView = document.getElementById('groupProjectView');
    const groupProjectLink = document.getElementById('groupProjectLink');
    const membersTable = document.getElementById('membersTable');
    const tbody = membersTable.querySelector('tbody');
    const addRowBtn = document.querySelector('.add-row-btn'); // Tombol Add

    function showView(viewToShow) {
        groupProjectView.style.display = 'none';
        viewToShow.style.display = 'block';
    }

    groupProjectLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(groupProjectView);
    });

    // Fungsi untuk menambahkan baris kosong dengan inputan kosong (termasuk Role)
    addRowBtn.addEventListener('click', function() {
        const newRow = tbody.insertRow();  // Menambahkan baris baru ke tabel

        // Menambahkan kolom inputan kosong untuk setiap kolom
        const nameCell = newRow.insertCell(0);
        const emailCell = newRow.insertCell(1);
        const phoneCell = newRow.insertCell(2);
        const roleCell = newRow.insertCell(3);  // Menambahkan kolom untuk Role

        nameCell.innerHTML = '<input type="text" placeholder="Enter name">';
        emailCell.innerHTML = '<input type="email" placeholder="Enter email">';
        phoneCell.innerHTML = '<input type="tel" placeholder="Enter phone">';
        
        // Tambahkan input untuk Role
        roleCell.innerHTML = '<select><option value="Admin">Admin</option><option value="Member">Member</option><option value="Guest">Guest</option></select>';
    });

    // Hapus data dari localStorage saat halaman akan ditutup atau direfresh
    window.addEventListener('beforeunload', function () {
        localStorage.removeItem('members'); // Menghapus data members di localStorage
    });

    // Ambil data anggota dari backend (Flask)
    fetch('/members')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Menambahkan data anggota ke dalam tabel
            data.forEach(member => {
                const newRow = tbody.insertRow();
                const nameCell = newRow.insertCell(0);
                const emailCell = newRow.insertCell(1);
                const phoneCell = newRow.insertCell(2);
                const roleCell = newRow.insertCell(3);

                nameCell.textContent = member.name;
                emailCell.textContent = member.email;
                phoneCell.textContent = member.phone;
                roleCell.textContent = member.role;
            });
        })
        .catch(error => {
            console.error('Error fetching members:', error);
            alert('There was an error fetching the members.');
        });
})