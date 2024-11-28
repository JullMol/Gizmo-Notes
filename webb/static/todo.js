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

    function initializeDayView() {
        const addButton = document.querySelector('#dayView #addButton');
        if (addButton) {
            addButton.addEventListener('click', addDayTask);
        }
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
    }
    
    const eventTasks = [];
    function addEventTask() {
        const dateInput = document.querySelector('#eventView #assignmentDate');
        const timeInput = document.querySelector('#eventView #assignmentTime');
        const locationInput = document.querySelector('#eventView #assignmentSubject');
        const detailsInput = document.querySelector('#eventView #assignmentDetails');
        const priorityInput = document.querySelector('#eventView #eventPriority');
    
        // Validasi input
        if (!dateInput.value || !timeInput.value || !locationInput.value || !detailsInput.value) {
            alert('Please fill in all fields');
            return;
        }
    
        // Buat objek tugas
        const task = {
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