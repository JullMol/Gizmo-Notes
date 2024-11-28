document.addEventListener('DOMContentLoaded', function() {
    const DayLink = document.getElementById('DayLink');
    const dayView = document.getElementById('dayView');
    const assignmentView = document.getElementById('assignmentView');
    const AssignmentLink = document.getElementById('AssignmentLink');
    const eventView = document.getElementById('eventView');
    const EventLink = document.getElementById('EventLink');

    function showView(viewToShow) {
        dayView.style.display = 'none';
        assignmentView.style.display = 'none';
        eventView.style.display = 'none';
        viewToShow.style.display = 'block';
    }

    DayLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(dayView)
    });

    AssignmentLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(assignmentView)
    });

    EventLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(eventView)
    });

    // Fungsi untuk memuat tugas dari localStorage
    function loadTasksFromLocalStorage(storageKey, tableSelector) {
        const tasks = JSON.parse(localStorage.getItem(storageKey) || '[]');
        const tableBody = document.querySelector(tableSelector);
        tableBody.innerHTML = ''; // Bersihkan tabel sebelum memuat

        tasks.forEach(task => {
            const newRow = document.createElement('tr');
            newRow.setAttribute('data-id', task.id);
            
            // Sesuaikan dengan struktur masing-masing tabel
            if (storageKey === 'dayTasks') {
                newRow.innerHTML = `
                    <td>${task.date}</td>
                    <td>${task.time}</td>
                    <td>${task.placement}</td>
                    <td>${task.activities}</td>
                    <td>${task.priority}</td>
                    <td><button class="deleteButton">Delete</button></td>
                `;
            } else if (storageKey === 'assignmentTasks') {
                newRow.innerHTML = `
                    <td>${task.date}</td>
                    <td>${task.time}</td>
                    <td>${task.subject}</td>
                    <td>${task.details}</td>
                    <td>${task.priority}</td>
                    <td><button class="deleteButton">Delete</button></td>
                `;
            } else if (storageKey === 'eventTasks') {
                newRow.innerHTML = `
                    <td>${task.date}</td>
                    <td>${task.time}</td>
                    <td>${task.location}</td>
                    <td>${task.details}</td>
                    <td>${task.priority}</td>
                    <td><button class="deleteButton">Delete</button></td>
                `;
            }

            // Tambahkan event listener untuk tombol delete
            const deleteButton = newRow.querySelector('.deleteButton');
            deleteButton.addEventListener('click', function() {
                // Hapus dari localStorage
                const tasks = JSON.parse(localStorage.getItem(storageKey) || '[]');
                const filteredTasks = tasks.filter(t => t.id !== task.id);
                localStorage.setItem(storageKey, JSON.stringify(filteredTasks));
                
                // Hapus baris dari tabel
                newRow.remove();
            });

            tableBody.appendChild(newRow);
        });
    }

    function initializeDayView() {
        const addButton = document.querySelector('#dayView #addButton');
        if (addButton) {
            addButton.addEventListener('click', addDayTask);
        }
        // Muat tugas dari localStorage
        loadTasksFromLocalStorage('dayTasks', '#taskTable tbody');
    }
    
    function addDayTask() {
        const dateInput = document.querySelector('#dayView #taskDate');
        const timeInput = document.querySelector('#dayView #taskTime');
        const placementInput = document.querySelector('#dayView #taskPlace');
        const activitiesInput = document.querySelector('#dayView #taskActivities');
        const priorityInput = document.querySelector('#dayView #taskPriority');
    
        // Validasi input
        if (!dateInput.value || !timeInput.value || !placementInput.value || !activitiesInput.value) {
            alert('Please fill in all fields');
            return;
        }
    
        // Buat objek tugas
        const task = {
            id : Date.now(),
            date: dateInput.value,
            time: timeInput.value,
            placement: placementInput.value,
            activities: activitiesInput.value,
            priority: priorityInput.value
        };
    
        // Kirim tugas ke backend
        fetch('/save_day_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(task)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                 // Simpan ke localStorage
                 let dayTasks = JSON.parse(localStorage.getItem('dayTasks') || '[]');
                 dayTasks.push(task);
                 localStorage.setItem('dayTasks', JSON.stringify(dayTasks));

                // Tambahkan baris baru ke tabel
                const taskTableBody = document.querySelector('#taskTable tbody');
                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>${task.date}</td>
                    <td>${task.time}</td>
                    <td>${task.placement}</td>
                    <td>${task.activities}</td>
                    <td>${task.priority}</td>
                    <td><button class="deleteButton">Delete</button></td>
                `;
                taskTableBody.appendChild(newRow);

                // Tambahkan event listener untuk tombol delete
                newRow.querySelector('.deleteButton').addEventListener('click', function() {
                    // Hapus dari localStorage
                    let dayTasks = JSON.parse(localStorage.getItem('dayTasks') || '[]');
                    dayTasks = dayTasks.filter(t => t.id !== task.id);
                    localStorage.setItem('dayTasks', JSON.stringify(dayTasks));

                    newRow.remove();
                });
    
                // Kosongkan input
                dateInput.value = '';
                timeInput.value = '';
                placementInput.value = '';
                activitiesInput.value = '';
                priorityInput.value = 'low';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Gagal menyimpan tugas');
        });
    }
    
    // Panggil fungsi untuk menginisialisasi Day View
    initializeDayView();
    
    function initializeAssignmentView() {
        const addAssignmentButton = document.querySelector('#assignmentView #addAssignmentButton');
        if (addAssignmentButton) {
            addAssignmentButton.addEventListener('click', addAssignmentTask);
        }
        // Muat tugas dari localStorage
        loadTasksFromLocalStorage('assignmentTasks', '#assignmentTable tbody');
    }
    
    function addAssignmentTask() {
        const dateInput = document.querySelector('#assignmentView #assignmentDate');
        const timeInput = document.querySelector('#assignmentView #assignmentTime');
        const subjectInput = document.querySelector('#assignmentView #assignmentSubject');
        const detailsInput = document.querySelector('#assignmentView #assignmentDetails');
        const priorityInput = document.querySelector('#assignmentView #assignmentPriority');
    
        // Validasi input
        if (!dateInput.value || !timeInput.value || !subjectInput.value || !detailsInput.value) {
            alert('Please fill in all fields');
            return;
        }
    
        // Buat objek tugas
        const task = {
            id : Date.now(),
            date: dateInput.value,
            time: timeInput.value,
            subject: subjectInput.value,
            details: detailsInput.value,
            priority: priorityInput.value
        };
    
        // Kirim tugas ke backend
        fetch('/save_assignment_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(task)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                 // Simpan ke localStorage
                 let assignmentTasks = JSON.parse(localStorage.getItem('assignmentTasks') || '[]');
                 assignmentTasks.push(task);
                 localStorage.setItem('assignmentTasks', JSON.stringify(assignmentTasks));

                // Tambahkan baris baru ke tabel
                const assignmentTableBody = document.querySelector('#assignmentTable tbody');
                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>${task.date}</td>
                    <td>${task.time}</td>
                    <td>${task.subject}</td>
                    <td>${task.details}</td>
                    <td>${task.priority}</td>
                    <td><button class="deleteButton">Delete</button></td>
                `;
                assignmentTableBody.appendChild(newRow);

                // Tambahkan event listener untuk tombol delete
                newRow.querySelector('.deleteButton').addEventListener('click', function() {
                    // Hapus dari localStorage
                    let assignmentTasks = JSON.parse(localStorage.getItem('assignmentTasks') || '[]');
                    assignmentTasks = assignmentTasks.filter(t => t.id !== task.id);
                    localStorage.setItem('assignmentTasks', JSON.stringify(assignmentTasks));

                    newRow.remove();
                });
    
                // Kosongkan input
                dateInput.value = '';
                timeInput.value = '';
                subjectInput.value = '';
                detailsInput.value = '';
                priorityInput.value = 'low';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Gagal menyimpan tugas');
        });
    }
    
    // Panggil fungsi untuk menginisialisasi Assignment View
    initializeAssignmentView();
    
    function initializeEventView() {
        const addEventButton = document.querySelector('#eventView #addEventButton');
        if (addEventButton) {
            addEventButton.addEventListener('click', addEventTask);
        }
        // Muat tugas dari localStorage
        loadTasksFromLocalStorage('eventTasks', '#eventTable tbody');
    }
    
    function addEventTask() {
        const dateInput = document.querySelector('#eventView #EventDate');
        const timeInput = document.querySelector('#eventView #EventTime');
        const locationInput = document.querySelector('#eventView #EventSubject');
        const detailsInput = document.querySelector('#eventView #EventDetails');
        const priorityInput = document.querySelector('#eventView #eventPriority');
    
        // Validasi input
        if (!dateInput.value || !timeInput.value || !locationInput.value || !detailsInput.value) {
            alert('Please fill in all fields');
            return;
        }
    
        // Buat objek tugas
        const task = {
            id : Date.now(),
            date: dateInput.value,
            time: timeInput.value,
            location: locationInput.value,
            details: detailsInput.value,
            priority: priorityInput.value
        };
    
        // Kirim tugas ke backend
        fetch('/save_event_task', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(task)
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Simpan ke localStorage
                let eventTasks = JSON.parse(localStorage.getItem('eventTasks') || '[]');
                eventTasks.push(task);
                localStorage.setItem('eventTasks', JSON.stringify(eventTasks));

                // Tambahkan baris baru ke tabel
                const eventTableBody = document.querySelector('#eventTable tbody');
                const newRow = document.createElement('tr');
                newRow.innerHTML = `
                    <td>${task.date}</td>
                    <td>${task.time}</td>
                    <td>${task.location}</td>
                    <td>${task.details}</td>
                    <td>${task.priority}</td>
                    <td><button class="deleteButton">Delete</button></td>
                `;
                eventTableBody.appendChild(newRow);

                // Tambahkan event listener untuk tombol delete
                newRow.querySelector('.deleteButton').addEventListener('click', function() {
                     // Hapus dari localStorage
                     let eventTasks = JSON.parse(localStorage.getItem('eventTasks') || '[]');
                     eventTasks = eventTasks.filter(t => t.id !== task.id);
                     localStorage.setItem('eventTasks', JSON.stringify(eventTasks));

                    newRow.remove();
                });
    
                // Kosongkan input
                dateInput.value = '';
                timeInput.value = '';
                locationInput.value = '';
                detailsInput.value = '';
                priorityInput.value = 'low';
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('Gagal menyimpan tugas');
        });
    }
    
    // Panggil fungsi untuk menginisialisasi Event View
    initializeEventView();
})