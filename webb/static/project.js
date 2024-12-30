var project = []

function fetchTasks(date = null) {
    url = '/getproject'
    fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched tasks:', data); // Debug
            project = data.tasks; // Simpan daftar tugas
            // console.log(tasks)
            // renderTaskList(); // Render tugas di tabel

            project.forEach(i => {
                renderList(i.project_name, i.session2, i.start, i.end)
            });
        })
        .catch(error => {
            console.error('Error fetching tasks:', error);
            alert('Failed to load tasks');
        });
}

fetchTasks()
function renderList(projectName, sessionTime, timeCreated, timeFinished) {
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

    // Fungsi untuk memformat waktu
    const formatDateTime = (date) => {
        const d = new Date(date);
        if (isNaN(d.getTime())) {
            console.error(`Invalid date: ${date}`); // Debug untuk melihat masalah
            return 'Invalid Date'; // Tangani nilai yang tidak valid
        }
        const day = String(d.getDate()).padStart(2, '0');
        const month = String(d.getMonth() + 1).padStart(2, '0'); // Bulan dimulai dari 0
        const year = d.getFullYear();
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const seconds = String(d.getSeconds()).padStart(2, '0');
        return `${day}-${month}-${year} ${hours}:${minutes}:${seconds}`;
    };

    // Format waktu dengan validasi
    timeCreatedCell.innerHTML = formatDateTime(timeCreated);
    timeFinishedCell.innerHTML = formatDateTime(timeFinished);

    const finishedTime = new Date(timeFinished).getTime();
    const now = new Date().getTime();

    if (now >= finishedTime) {
        statusCell.innerHTML = 'Time Out';
        statusCell.style.color = 'red'; // Warna merah untuk Time Out
    } else {
        statusCell.innerHTML = 'Pending';
        statusCell.style.color = 'yellow'; // Warna kuning untuk Pending
    }

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'delete-btn1';
    deleteBtn.innerHTML = 'Delete';
    deleteBtn.onclick = function () {
        fetch(`/delete_project?id=${row.rowIndex}`).then(response => response.json()).then(data => alert(data.message));
        table.deleteRow(row.rowIndex);
    };
    actionCell.appendChild(deleteBtn);
}



function addProject() {
    const projectName = document.getElementById('projectName').value;
    const sessionTime = document.getElementById('sessionTime').value;
    const timeCreated = document.getElementById('timeCreated').value;
    const timeFinished = document.getElementById('timeFinished').value;

    if (projectName && sessionTime && timeCreated && timeFinished) {
        // save
        fetch('/saveproject', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                projekname : projectName,
                session2 : sessionTime,
                timeCreated : timeCreated,
                timeFinished : timeFinished,
            })
        }).then(() => {
            window.location.reload()
        })

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