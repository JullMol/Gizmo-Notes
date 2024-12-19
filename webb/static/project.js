function addProject() {
    const projectName = document.getElementById('projectName').value;
    const sessionTime = document.getElementById('sessionTime').value;
    const timeCreated = document.getElementById('timeCreated').value;
    const timeFinished = document.getElementById('timeFinished').value;

    if (projectName && sessionTime && timeCreated && timeFinished) {
        const table = document.getElementById('projectTable');
        const row = table.insertRow();
        const projectCell = row.insertCell(0);
        const sessionCell = row.insertCell(1);
        const statusCell = row.insertCell(2);
        const timeCreatedCell = row.insertCell(3);
        const timeFinishedCell = row.insertCell(4);
        const actionCell = row.insertCell(5);

        projectCell.innerHTML = projectName;
        sessionCell.innerHTML = sessionTime;

        // Gunakan format ISO untuk waktu
        timeCreatedCell.innerHTML = new Date(timeCreated).toISOString();
        timeFinishedCell.innerHTML = new Date(timeFinished).toISOString();

        const finishedTime = new Date(timeFinished).getTime();
        const now = new Date().getTime();

        if (now >= finishedTime) {
            statusCell.innerHTML = 'Time Out';
            statusCell.style.color = 'red'; // Warna merah untuk Time Out
        } else {
            statusCell.innerHTML = 'Pending';
            statusCell.style.color = 'yellow'; // Warna hijau untuk Pending
        }

        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'delete-btn';
        deleteBtn.innerHTML = 'Delete';
        deleteBtn.onclick = function() {
            table.deleteRow(row.rowIndex);
        };
        actionCell.appendChild(deleteBtn);

        // Reset input form
        document.getElementById('projectName').value = '';
        document.getElementById('sessionTime').value = '';
        document.getElementById('timeCreated').value = '';
        document.getElementById('timeFinished').value = '';
    } else {
        alert('Please fill in all fields');
    }
}

function updateStatus() {
    const table = document.getElementById('projectTable');
    const rows = table.rows;
    const now = new Date().getTime();

    for (let i = 1; i < rows.length; i++) { // Mulai dari baris kedua karena baris pertama adalah header
        const timeFinishedCell = rows[i].cells[4];
        const statusCell = rows[i].cells[2];

        const finishedTime = new Date(timeFinishedCell.innerHTML).getTime();

        if (now >= finishedTime) {
            statusCell.innerHTML = 'Time Out';
            statusCell.style.color = 'red'; // Warna merah untuk Time Out
        } else {
            statusCell.innerHTML = 'Pending';
            statusCell.style.color = 'yellow'; // Warna hijau untuk Pending
        }
    }
}

// Jalankan fungsi pemantauan setiap detik
setInterval(updateStatus, 1000);