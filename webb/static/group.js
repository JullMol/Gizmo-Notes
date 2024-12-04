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
        window.location.href = '/invite'; // Ganti path sesuai kebutuhan
    });    

    addSchBtn.addEventListener('click', function() {
        saveData();
        const newRow1 = tbody1.insertRow();  // Menambahkan baris baru ke tabel

        const dateCell = newRow1.insertCell(0);
        const subjectCell = newRow1.insertCell(1);
        const linkCell = newRow1.insertCell(2);
        const actionCell = newRow1.insertCell(3);

        dateCell.innerHTML = '<input type="date">';
        subjectCell.innerHTML = '<input type="text" placeholder="Enter subject">';
        linkCell.innerHTML = '<input type="url" placeholder="Enter link">';
        linkCell.querySelector('input').addEventListener('input', function(event) {
            const input = event.target.value;

            if (input === '!bot') {
                fetch('/api/bot_invite')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Failed to fetch bot invite link');
                        }
                        return response.json();
                    })
                    .then(data => {
                        // Ubah nilai input menjadi tautan bot
                        event.target.value = data.invite_link;
                    })
                    .catch(error => {
                        console.error('Error fetching bot invite link:', error);
                        alert('Error fetching bot invite link.');
                    });
            }
        });
        const deleteButton = document.createElement('button');
        deleteButton.textContent = 'Delete';
        deleteButton.addEventListener('click', function () {
            newRow1.remove(); // Hapus baris dari tabel
        });
        actionCell.appendChild(deleteButton);
    })
        // Saat data diinput, langsung disimpan ke backend
        function saveData(){
            const all_row = tbody1.querySelectorAll('tr')
            all_row.forEach((row)=>{
                const scheduleData = {
                    date: row.cells[0].querySelector('input').value,
                    subject: row.cells[1].querySelector('input').value,
                    link: row.cells[2].querySelector('input').value
                };
                console.log(`date: ${scheduleData.date}, subject: ${scheduleData.subject}, link: ${scheduleData.link}`);
                console.log(scheduleData)
                if (!scheduleData.date || !scheduleData.subject || !scheduleData.link) {
                    alert('All fields are required!');
                    return;
                }
                fetch('/api/add_schedule', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(scheduleData)
                })
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Failed to save schedule');
                    }
                    return response.json();
                })
                .then(data => {
                    alert(data.message);
                })
                .catch(error => {
                    console.error('Error:', error);
                    alert('Failed to save the schedule.');
                });
            });
        };

        function deleteRow(row) {
            const table = row.parentNode.parentNode; // Ambil referensi tabel
            const tbody = table.querySelector('tbody');
        
            // Hapus baris
            row.remove();
        
            // Sembunyikan tabel jika tbody kosong
            if (!tbody.hasChildNodes()) {
                table.style.display = 'none';
            }
        }        

    // Tambahkan event listener pada input kolom link
    tbody1.addEventListener('input', function(event) {
        const target = event.target;

        // Periksa apakah input di kolom link
        if (target.tagName === 'INPUT' && target.type === 'url') {
            // Periksa jika input adalah "!bot"
            if (target.value === '!bot') {
                fetch('/api/bot_invite')
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json();
                    })
                    .then(data => {
                        // Ganti nilai input dengan tautan dari backend
                        target.value = data.invite_link;
                    })
                    .catch(error => {
                        console.error('Error fetching bot invite link:', error);
                        alert('Failed to fetch the bot invite link.');
                    });
            }
        }
    });

    // Hapus data dari localStorage saat halaman akan ditutup atau direfresh
    window.addEventListener('beforeunload', function () {
        localStorage.removeItem('members'); // Menghapus data members di localStorage
    });

    // Sembunyikan tabel jika tidak ada data
    if (!tbody.hasChildNodes()) {
        membersTable.style.display = 'none';
    }

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
            Object.values(data).forEach(member => {
                const newRow = tbody.insertRow();
                const nameCell = newRow.insertCell(0);
                const emailCell = newRow.insertCell(1);
                const phoneCell = newRow.insertCell(2);
                const roleCell = newRow.insertCell(3);
                const actionCell = newRow.insertCell(4);

                nameCell.textContent = member.name;
                emailCell.textContent = member.email;
                phoneCell.textContent = member.phone;
                roleCell.textContent = member.role;

                const deleteButton = document.createElement('button');
                deleteButton.textContent = 'Delete';
                deleteButton.addEventListener('click', function () {
                    fetch(`/api/members/${member.name}`, { method: 'GET' })
                        .then(response => {
                            if (!response.ok) throw new Error('Failed to delete member');
                            newRow.remove();
                            alert('Member deleted successfully');
                        })
                        .catch(error => {
                            console.error('Error deleting member:', error);
                            alert('Failed to delete member.');
                        });
                });
                actionCell.appendChild(deleteButton);
            });
        })
        .catch(error => {
            console.error('Error fetching members:', error);
            alert('There was an error fetching the members.');
        });
})