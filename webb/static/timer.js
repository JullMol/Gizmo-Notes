document.addEventListener('DOMContentLoaded', function () {
    const timerView = document.getElementById('timerView');
    const timerLink = document.getElementById('timerLink');
    // Ambil elemen-elemen DOM yang dibutuhkan
    const timeDisplay = document.querySelector('.time span');
    const playButton = document.querySelector('.play-button');
    const resetButton = document.querySelector('.reset-timer');
    const createGoals = document.getElementById('page-goals');
    const timeManagementTableBody = document.querySelector('.time-management-table-body');
    const taskInput = document.querySelector('.task-input');
    populateHours('.hour-start');
    populateHours('.hour-end');
    populateMinutes('.minute-start');
    populateMinutes('.minute-end');
    const saveTimeSlotButton = document.querySelector('.save-time-slot');
    const currentDate = document.querySelector('.current-date');
    const datePicker = document.querySelector('.date-picker');
    const calendarMonthYear = document.querySelector('.calendar-month-year');
    const calendarGrid = document.querySelector('.calendar-grid');

    function showView(viewToShow) {
        timerView.style.display = 'none';
        viewToShow.style.display = 'block';
    }

    timerLink.addEventListener('click', function(e) {
        e.preventDefault();
        showView(timerView);
    });

    // Validasi elemen yang harus ada
    if (!timeDisplay || !playButton || !resetButton || !timeManagementTableBody || !taskInput || 
        !saveTimeSlotButton || !currentDate || !datePicker || !calendarMonthYear || !calendarGrid) {
        console.error('Salah satu elemen penting untuk timer atau kalender tidak ditemukan.');
        return;
    }

    // Variabel untuk timer
    let remainingTime = 0;
    let timerRunning = false;
    let timer;
    let tasks = [];
    let taskDuration = [];
    let currentTaskIndex = 0;
    let breakTime = 5 * 60; // 5 menit break time
    let totalDuration = 0;
    let isBreak = false;

    createGoals.addEventListener('click', function () {
        window.location.href = '/page-goals';
    });

    function fetchTasks() {
        fetch('/tasks')
            .then(response => response.json())
            .then(data => {
                console.log('Fetched tasks:', data); // Debug
                tasks = data; // Simpan daftar tugas
                renderTaskList(); // Render tugas di tabel
            })
            .catch(error => {
                console.error('Error fetching tasks:', error);
                alert('Failed to load tasks');
            });
    }

    // Fungsi Timer
    function updateTimerDisplay(timeInSeconds) {
        const hours = Math.floor(timeInSeconds / 3600);
        const minutes = Math.floor((timeInSeconds % 3600) / 60);
        const seconds = timeInSeconds % 60;
        timeDisplay.textContent = `${String(hours).padStart(2, '0')} : ${String(minutes).padStart(2, '0')} : ${String(seconds).padStart(2, '0')}`;
    }

    // Di dalam event listener DOMContentLoaded
    window.startTask = function(taskId) {
        fetch(`/start-task/${taskId}`, {method:'POST'})
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // Update status tugas di frontend
                tasks = tasks.map(task => 
                    task.id === taskId 
                        ? {...task, status: 'running'} 
                        : {...task, status: task.status === 'running' ? 'pending' : task.status}
                );
                
                // Perbarui tampilan
                renderTaskList();
                
                // Jalankan timer untuk tugas spesifik
                const currentTask = tasks.find(task => task.id === taskId);
                if (currentTask) {
                    startTimer(currentTask.duration * 60);
                }
                
                // Opsional: Lanjutkan ke task berikutnya secara otomatis
                // Uncomment jika Anda ingin menjalankan semua task berurutan
                // autoProgressTasks(); 
            } else {
                alert(data.message);
            }
        })
        .catch(error => {
            console.error('Error starting task:', error);
            alert('Failed to start task');
        });
    };

    function renderTaskList() {
        const taskTableBody = document.querySelector('.time-management-table-body');
        taskTableBody.innerHTML = ''; // Kosongkan tabel sebelum diperbarui
    
        // Urutkan tugas berdasarkan waktu mulai
        const sortedTasks = tasks.sort((a, b) => {
            // Parsing waktu dengan benar
            const parseTime = (timeStr) => {
                const [time, period] = timeStr.split(' ');
                let [hours, minutes] = time.split(':').map(Number);
                
                if (period === 'PM' && hours !== 12) hours += 12;
                if (period === 'AM' && hours === 12) hours = 0;
                
                return hours * 60 + minutes;
            };
    
            return parseTime(a.startTime) - parseTime(b.startTime);
        });
    
        sortedTasks.forEach((task, index) => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${task.startTime} - ${task.endTime}</td>
                <td>${task.description}</td>
                <td>${task.status || 'pending'}</td>
                <td>
                    <button onclick="startTask(${task.id})" 
                            ${task.status === 'running' ? 'disabled' : ''}>
                        Start
                    </button>
                </td>
            `;
            taskTableBody.appendChild(row);
        });
    }

    function autoProgressTasks() {
        let currentTaskIndex = 0;
    
        function runNextTask() {
            if (currentTaskIndex < tasks.length) {
                const currentTask = tasks[currentTaskIndex];
                
                // Jalankan tugas saat ini
                startTimer(currentTask.duration * 60);
    
                // Event listener untuk menandakan tugas selesai
                const taskCompleteHandler = () => {
                    // Hapus event listener untuk mencegah multiple calls
                    playButton.removeEventListener('click', taskCompleteHandler);
    
                    // Tambahkan break time
                    setTimeout(() => {
                        // Jalankan break time
                        remainingTime = breakTime;
                        updateTimerDisplay(remainingTime, true);
                        
                        // Setelah break, lanjut ke tugas berikutnya
                        setTimeout(() => {
                            currentTaskIndex++;
                            
                            if (currentTaskIndex < tasks.length) {
                                runNextTask(); // Lanjutkan ke tugas berikutnya
                            } else {
                                // Semua tugas selesai
                                alert('Semua tugas telah diselesaikan!');
                                resetTimerState();
                            }
                        }, breakTime * 1000);
                    }, currentTask.duration * 60 * 1000);
                };
    
                // Tambahkan event listener untuk mendeteksi kapan tugas selesai
                playButton.addEventListener('click', taskCompleteHandler);
            }
        }
    
        function resetTimerState() {
            clearInterval(timer);
            timerRunning = false;
            remainingTime = 0;
            currentTaskIndex = 0;
            isBreak = false;
            updateTimerDisplay(0);
            playButton.classList.remove('fa-pause');
            playButton.classList.add('fa-play-circle');
        
            // Hanya reset status tugas yang belum selesai
            tasks.forEach((task, index) => {
                if (task.status !== "Completed") {
                    task.status = "Pending";
                    updateTaskStatus(index, "Pending");
                }
            });
        }        
        
        // Mulai dari tugas pertama
        runNextTask();
    }

    // Fungsi untuk memulai tugas berikutnya
    function startNextTask() {
        if (currentTaskIndex < taskDurations.length) {
            const duration = taskDurations[currentTaskIndex];
            isBreak = false; // Reset status break
            startTimer(duration); // Mulai tugas
        } else {
            alert("Semua tugas telah selesai!");
            resetTimerState();
        }
    }

    // Fungsi untuk memperbarui status tugas di UI
    function updateTaskStatus(index, status) {
        tasks[index].status = status; // Perbarui status di array tugas
        const taskRows = document.querySelectorAll('.time-management-table-body tr');
        if (taskRows[index]) {
            const statusCell = taskRows[index].querySelector('td:nth-child(3)');
            if (statusCell) {
                statusCell.textContent = status; // Perbarui teks status di tabel UI
            }
        }
    }    

    function startTimer(duration) {
        if (!duration || isNaN(duration) || duration <= 0) {
            alert("Durasi tidak valid.");
            return;
        }
    
        if (timerRunning) {
            clearInterval(timer);
        }
    
        remainingTime = duration; // Set waktu awal
        timerRunning = true;
        playButton.classList.remove('fa-play-circle');
        playButton.classList.add('fa-pause');
    
        timer = setInterval(() => {
            if (remainingTime > 0) {
                remainingTime--;
                updateTimerDisplay(remainingTime, isBreak);
            } else {
                clearInterval(timer);
                timerRunning = false;
    
                if (!isBreak) {
                    // Saat tugas selesai
                    alert("Task selesai! Memulai waktu istirahat...");
                    updateTaskStatus(currentTaskIndex, "Completed");
    
                    // Jika ini tugas terakhir, langsung selesai tanpa break
                    if (currentTaskIndex === tasks.length - 1) {
                        alert("Semua tugas telah selesai!");
                        resetTimerState();
                        return;
                    }
    
                    // Mulai waktu istirahat untuk tugas selain terakhir
                    remainingTime = breakTime;
                    isBreak = true;
                    startTimer(remainingTime); // Mulai waktu istirahat
                } else {
                    // Setelah waktu istirahat selesai
                    alert("Waktu istirahat selesai.");
    
                    if (currentTaskIndex === tasks.length - 1) {
                        // Tugas terakhir: pastikan statusnya menjadi Completed
                        updateTaskStatus(currentTaskIndex, "Completed");
                        alert("Semua tugas telah selesai!");
                        resetTimerState();
                    } else {
                        // Pindah ke tugas berikutnya
                        currentTaskIndex++;
                        isBreak = false; // Reset status break
                        playButton.classList.remove('fa-pause');
                        playButton.classList.add('fa-play-circle');
                        timerRunning = false;
                        updateTimerDisplay(0);
                    }
                }
            }
        }, 1000);
    }    
    
    document.addEventListener('DOMContentLoaded', function () {
        fetchTasks(); // Ambil daftar tugas dari server
    });    
    
    // Tombol untuk memulai tugas saat ini
    playButton.addEventListener('click', function () {
        if (currentTaskIndex < taskDurations.length) {
            startNextTask();
        } else {
            alert("Semua tugas telah selesai!");
        }
    });

    resetButton.addEventListener('click', function () {
        clearInterval(timer);
        timerRunning = false;
        remainingTime = totalDuration; // Kembalikan ke durasi total
        updateTimerDisplay(remainingTime);
        playButton.classList.remove('fa-pause');
        playButton.classList.add('fa-play-circle');
    
        // Reset task di server
        fetch('/reset-task', { method: 'POST' })
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    fetchTasks(); // Perbarui daftar tugas
                }
            });
    });

    function formatTime(hour, minute, period) {
        const formattedHour = String(hour).padStart(2, '0');
        const formattedMinute = String(minute).padStart(2, '0');
        return `${formattedHour}:${formattedMinute} ${period}`;
    }

    function isTimeOverlap(newStart, newEnd, tasks) {
        for (const task of tasks) {
            const existingStart = new Date(`1970-01-01T${task.startTime}:00`);
            const existingEnd = new Date(`1970-01-01T${task.endTime}:00`);
            const existingBreakEnd = new Date(existingEnd.getTime() + 5 * 60 * 1000); // Tambahkan 5 menit break
    
            // Cek overlap
            if (newStart < existingBreakEnd && newEnd > existingStart) {
                return true;
            }
        }
        return false;
    }

    // Fungsi Menambah Tugas
    function addTimeSlot() {
        console.log('addTimeSlot() added');
        const startHour = document.querySelector('.hour-start').value;
        const startMinute = document.querySelector('.minute-start').value;
        const startPeriod = document.querySelector('.period-start').value;
        const endHour = document.querySelector('.hour-end').value;
        const endMinute = document.querySelector('.minute-end').value;
        const endPeriod = document.querySelector('.period-end').value;
        const task = taskInput.value.trim();

        if (startHour && startMinute && startPeriod && endHour && endMinute && endPeriod && task) {
            const formattedStartTime = `${startHour}:${startMinute} ${startPeriod}`;
            const formattedEndTime = `${endHour}:${endMinute} ${endPeriod}`;

            console.log('Sending data:', {
                taskDescription: task,
                startTime: formattedStartTime,
                endTime: formattedEndTime
            });

            // Send data to server
            fetch('/add-task', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    taskDescription: task,
                    startTime: formattedStartTime,
                    endTime: formattedEndTime,
                    date: selectedDate.toISOString().split('T')[0]
                })
            })
            .then(response => {
                if (!response.ok) {
                    return response.json().then(err => Promise.reject(err));
                }
                return response.json();
            })
            .then(data => {
                console.log('Server response:', data);
                
                if (data.status === 'success') {
                    // Add task to table
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td>${formattedStartTime} - ${formattedEndTime}</td>
                        <td>${task}</td>
                        <td>Pending</td>
                    `;
                    timeManagementTableBody.appendChild(row);

                    // Reset inputs
                    document.querySelector('.hour-start').value = '';
                    document.querySelector('.minute-start').value = '';
                    document.querySelector('.period-start').value = '';
                    document.querySelector('.hour-end').value = '';
                    document.querySelector('.minute-end').value = '';
                    document.querySelector('.period-end').value = '';
                    taskInput.value = '';
                } else {
                    alert('Failed to add task: ' + data.message);
                }
            })
            .catch(error => {
                console.error('Error details:', error);
                alert('An error occurred while adding the task. Please check the time format.');
            });
        } else {
            alert('Please fill in all fields before adding a task.');
        }
    }

    // Fungsi untuk menerima input durasi dari user
    function addTaskDuration(duration) {
        if (duration > 0) {
            taskDurations.push(duration);
            alert(`Tugas dengan durasi ${duration} detik ditambahkan.`);
        } else {
            alert("Durasi tugas harus lebih besar dari 0.");
        }
    }

    function populateHours(selector) {
        const hourDropdown = document.querySelector(selector);
        hourDropdown.innerHTML = ''; // Kosongkan dropdown sebelum mengisi ulang
        for (let i = 1; i <= 12; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i.toString().padStart(2, '0'); // Format 2 digit
            hourDropdown.appendChild(option);
        }
    }
    
    function populateMinutes(selector) {
        const minuteDropdown = document.querySelector(selector);
        minuteDropdown.innerHTML = ''; // Kosongkan dropdown sebelum mengisi ulang
        for (let i = 0; i < 60; i++) {
            const option = document.createElement('option');
            option.value = i;
            option.textContent = i.toString().padStart(2, '0'); // Format 2 digit
            minuteDropdown.appendChild(option);
        }
    }

    function updateTimerDisplay(timeInSeconds, isBreak = false) {
        const hours = Math.floor(timeInSeconds / 3600);
        const minutes = Math.floor((timeInSeconds % 3600) / 60);
        const seconds = timeInSeconds % 60;
        timeDisplay.textContent = `${String(hours).padStart(2, '0')} : ${String(minutes).padStart(2, '0')} : ${String(seconds).padStart(2, '0')}`;
    
        if (isBreak) {
            timeDisplay.style.color = 'green'; // Ganti warna untuk waktu istirahat
        } else {
            timeDisplay.style.color = 'yellow';
        }
    }    
    
    saveTimeSlotButton.addEventListener('click', addTimeSlot);

    function fetchTasksByDate(date) {
        fetch(`/data-by-date/${date}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    tasks = data.tasks;
                    renderTaskList();
                    fetchNotifications(date);
                } else {
                    alert("Gagal mengambil tugas: " + data.message);
                }
            })
            .catch(error => {
                console.error("Error fetching tasks by date:", error);
                alert("Terjadi kesalahan saat mengambil tugas.");
            });
    }

    function fetchTasks(date) {
        const url = date ? `/tasks?date=${date}` : '/tasks';
        fetch(url)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    tasks = data.tasks;
                    renderTaskList();
                } else {
                    alert('Gagal mengambil tugas: ' + data.message);
                }
            })
            .catch(error => console.error('Error fetching tasks:', error));
    }  

    // Fungsi Kalender
    let selectedDate = new Date();  

    function renderCalendar(date) {
        const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
        const lastDay = new Date(date.getFullYear(), date.getMonth() + 1, 0);
        const startingDay = firstDay.getDay();

        calendarMonthYear.textContent = date.toLocaleString('default', {
            month: 'long',
            year: 'numeric',
        });

        // Hapus hari sebelumnya
        calendarGrid.innerHTML = '';

        // Tambahkan sel kosong sebelum tanggal pertama
        for (let i = 0; i < startingDay; i++) {
            const emptyCell = document.createElement('div');
            emptyCell.classList.add('calendar-day');
            calendarGrid.appendChild(emptyCell);
        }

        // Tambahkan hari-hari dalam bulan
        for (let i = 1; i <= lastDay.getDate(); i++) {
            const dayCell = document.createElement('div');
            dayCell.classList.add('calendar-day');
            dayCell.textContent = i;

            if (i === date.getDate() &&
                date.getMonth() === selectedDate.getMonth() &&
                date.getFullYear() === selectedDate.getFullYear()) {
                dayCell.classList.add('current');
            }

            dayCell.addEventListener('click', () => {
                selectedDate = new Date(date.getFullYear(), date.getMonth(), i);
                const formattedDate = selectedDate.toISOString().split('T')[0];
                currentDate.textContent = selectedDate.toLocaleDateString('default', {
                    weekday: 'short',
                    month: 'short',
                    day: 'numeric',
                });
                datePicker.classList.remove('active');
                renderCalendar(selectedDate);
                fetchTasksByDate(formattedDate);
                fetchGoalsByDate(formattedDate);
            });

            calendarGrid.appendChild(dayCell);
        }
    }

    currentDate.addEventListener('click', () => {
        datePicker.classList.toggle('active');
        renderCalendar(selectedDate);
    });

    document.querySelector('.prev-month-picker').addEventListener('click', (e) => {
        e.stopPropagation();
        selectedDate.setMonth(selectedDate.getMonth() - 1);
        renderCalendar(selectedDate);
    });

    document.querySelector('.next-month-picker').addEventListener('click', (e) => {
        e.stopPropagation();
        selectedDate.setMonth(selectedDate.getMonth() + 1);
        renderCalendar(selectedDate);
    });

    document.addEventListener('click', (e) => {
        if (!datePicker.contains(e.target) && !currentDate.contains(e.target)) {
            datePicker.classList.remove('active');
        }
    });

    // Render kalender awal
    renderCalendar(selectedDate); 

    function fetchNotifications(date) {
        fetch(`/notifications/${date}`)
            .then(response => response.json())
            .then(data => {
                if (data.status === 'success') {
                    scheduleNotifications(data.notifications);
                } else {
                    alert('Gagal mengambil notifikasi: ' + data.message);
                }
            })
            .catch(error => console.error('Error fetching notifications:', error));
    }
    
    function scheduleNotifications(notifications) {
        notifications.forEach(notification => {
            const now = new Date();
            const targetTime = new Date();
            const [hours, minutes, seconds] = notification.time.split(':').map(Number);
            targetTime.setHours(hours, minutes, seconds);
    
            const delay = targetTime - now;
    
            if (delay > 0) {
                console.log(`Notification scheduled in ${delay} ms: ${notification.message}`); // Debug log
                setTimeout(() => {
                    if (Notification.permission === "granted") {
                        new Notification(notification.message);
                    } else {
                        alert(notification.message);
                    }                    
                    console.log(notification.message); // Debug log
                }, delay);
            } else {
                console.log(`Notification skipped (past time): ${notification.message}`);
            }
        });
    }    

    function requestNotificationPermission() {
        if ("Notification" in window) {
            Notification.requestPermission().then(permission => {
                if (permission === "granted") {
                    console.log("Notification permission granted.");
                } else {
                    alert("Please allow notifications to receive task reminders.");
                }
            });
        } else {
            alert("Browser does not support notifications.");
        }
    }
    
    document.addEventListener('DOMContentLoaded', requestNotificationPermission);    
});
