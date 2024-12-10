let waktutertentu = new Date();
let selectedDates = {};
selDate = `${waktutertentu.getFullYear()}-${waktutertentu.getMonth()}-${("0" + waktutertentu.getDay()).slice(-2)}`
let sessions = [
    { id: 1, name: 'Grocery Shop', color: '#60a5fa' },
    { id: 2, name: 'Meeting', color: '#f472b6' },
    { id: 3, name: 'Lunch', color: '#9ca3af' }
];

let currentSessionId = 1;
let nextSessionId = 4;

function initCalendar() {
    const calendar = document.getElementById('calendar');
    const monthDisplay = document.getElementById('monthDisplay');
            
    const firstDay = new Date(waktutertentu.getFullYear(), waktutertentu.getMonth(), 1);
    const lastDay = new Date(waktutertentu.getFullYear(), waktutertentu.getMonth() + 1, 0);
            
    monthDisplay.textContent = `${waktutertentu.toLocaleString('default', { month: 'short' })} . ${waktutertentu.getFullYear()}`;
            
    calendar.innerHTML = '';
            
    for (let i = 0; i < firstDay.getDay(); i++) {
        calendar.appendChild(document.createElement('div'));
    }
            
    for (let day = 1; day <= lastDay.getDate(); day++) {
        const dayElement = document.createElement('div');
        dayElement.textContent = day;
        dayElement.classList.add('day');
                
        const dateString = `${waktutertentu.getFullYear()}-${waktutertentu.getMonth()}-${("0" + waktutertentu.getDay()).slice(-2)}`;
        if (selectedDates[dateString]) {
            const session = sessions.find(s => s.id === selectedDates[dateString]);
            if (session) {
                dayElement.classList.add('has-session');
                dayElement.style.backgroundColor = session.color;
            }
        }
                
        const dayOfWeek = new Date(waktutertentu.getFullYear(), waktutertentu.getMonth(), day).getDay();
        if (dayOfWeek === 0 || dayOfWeek === 6) {
            dayElement.classList.add('weekend');
        }
                
        dayElement.addEventListener('click', () => toggleDate(day));
        calendar.appendChild(dayElement);
    }

    updateSessionList();
}

async function updateSessionList() {
    const sessionList = document.getElementById('sessionList');
    sessionList.innerHTML = '';

    all = await fetch('/getcalendar')
        .then(response => response.json())
        .then(data => {
            console.log('Fetched tasks:', data); // Debug
            project = data.tasks; // Simpan daftar tugas
            // console.log(tasks)
            // renderTaskList(); // Render tugas di tabel

            project.forEach(i => {
                const sessionElement = document.createElement('div');
                sessionElement.className = 'session-type';
                if (i.id === currentSessionId) {
                    sessionElement.classList.add('selected-session');
                }
                        
                sessionElement.innerHTML = `
                <div class="session-indicator" style="background-color: ${i.colour}"></div>
                <span>${i.name}</span>
                <button class="delete-btn" onclick="deleteSession(${i.id})">×</button>
                `;
                        
                sessionElement.addEventListener('click', () => selectSession(session.id));
                // sessionList.appendChild(sessionElement);

                console.log(i.dt, selDate)
                if (i.dt == selDate) {
                    sessionList.appendChild(sessionElement);
                }
            });
        })
}

function showAddSessionForm() {
    document.getElementById('sessionForm').style.display = 'block';
    document.getElementById('sessionName').value = '';
    document.getElementById('sessionColor').value = '#3b82f6';
}

function cancelSessionForm() {
    document.getElementById('sessionForm').style.display = 'none';
}

function saveSession() {
    const name = document.getElementById('sessionName').value.trim();
    const color = document.getElementById('sessionColor').value;
            
    if (name) {
        sessions.push({
        id: nextSessionId++,
        name: name,
        color: color
        });

        fetch('/calendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name : name,
                colour : color,
                tanggal : selDate,
            })
        }).then(() => {
            window.location.reload()
        })

        cancelSessionForm();
        updateSessionList();
    }
}

function deleteSession(id) {
    event.stopPropagation();
    if (sessions.length > 1) {
        sessions = sessions.filter(s => s.id !== id);
            if (currentSessionId === id) {
                currentSessionId = sessions[0].id;
            }
            // Remove deleted session from dates
            for (let dateStr in selectedDates) {
                if (selectedDates[dateStr] === id) {
                    delete selectedDates[dateStr];
                }
            }
            initCalendar();
    }
}

function selectSession(id) {
    currentSessionId = id;
    updateSessionList();
}

function toggleDate(day) {
    const dateString = `${waktutertentu.getFullYear()}-${waktutertentu.getMonth()}-${("0" + day).slice(-2)}`;
    selDate = dateString
    if (selectedDates[dateString] === currentSessionId) {
        delete selectedDates[dateString];
    } else {
        selectedDates[dateString] = currentSessionId;
    }
    initCalendar();
}

function prevMonth() {
    waktutertentu.setMonth(waktutertentu.getMonth() - 1);
    initCalendar();
}

function nextMonth() {
    waktutertentu.setMonth(waktutertentu.getMonth() + 1);
    initCalendar();
}

// Initialize calendar on load
initCalendar();