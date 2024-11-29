document.addEventListener('DOMContentLoaded', function() {
    const groupProjectView = document.getElementById('groupProjectView');
    const groupProjectLink = document.getElementById('groupProjectLink');
    const membersTable = document.getElementById('membersTable');
    const scheduleTable = document.getElementById('scheduleTable')
    const tbody = membersTable.querySelector('tbody');
    const tbody1 = scheduleTable.querySelector('tbody');
    const addRowBtn = document.querySelector('.add-row-btn'); // Tombol Add
    const addSchBtn = document.querySelector('.add-sch-btn');
    

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

    addSchBtn.addEventListener('click', function() {
        const newRow1 = tbody1.insertRow();  // Menambahkan baris baru ke tabel

        const dateCell = newRow1.insertCell(0);
        const subjectCell = newRow1.insertCell(1);
        const linkCell = newRow1.insertCell(2);

        dateCell.innerHTML = '<input type="date">';
        subjectCell.innerHTML = '<input type="text" placeholder="Enter subject">';
        linkCell.innerHTML = '<input type="url" placeholder="Enter link">';
        let isValid = true;
    })

    // Hapus data dari localStorage saat halaman akan ditutup atau direfresh
    window.addEventListener('beforeunload', function () {
        localStorage.removeItem('members'); // Menghapus data members di localStorage
    });

    // Ambil data anggota dari backend (Flask)
    fetch('/api/members')
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

    if (isValid) {
        const scheduleData = {
            date: dateCell,
            subject: subjectCell,
            link: linkCell
        };
        console.log('Schedule Data:', scheduleData)

        fetch('/api/add_schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(scheduleData)
        })
        .then(response => {
            if (!response.ok) { // Jika status bukan 2xx, maka ada error
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            alert(data.message);  // Menampilkan pesan sukses dari backend
            resetForm();  // Reset form setelah sukses
        })
        .catch(error => {
            console.error('Error:', error);
            alert('There was an error adding the member.');
        });
    }
})