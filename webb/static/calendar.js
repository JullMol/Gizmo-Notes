let waktutertentu = new Date();
let selectedDates = {};
let sessions = [];

let currentSessionId = 1;
// let nextSessionId = 2;

async function initCalendar() {
    await updateSessionList();
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
                
        const dateString = `${waktutertentu.getFullYear()}-${waktutertentu.getMonth()}-${("0" + day).slice(-2)}`;
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

}

async function updateSessionList() {
    const sessionList = document.getElementById('sessionList');
    sessionList.innerHTML = '';
    sessions = []
    all = await fetch('/getcalendar')
        .then(response => response.json())
        .then(data => {
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
            
                sessionElement.addEventListener('click', () => selectSession(i.id)); // Menggunakan `i.id`
                sessionList.appendChild(sessionElement);
                if (i.date){
                    i.date.forEach(tgl => selectedDates[tgl]=i.id)
                }
                sessions.push({
                    'id': i.id,
                    'name': i.name,
                    'color': i.colour
                });
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

function saveSession(select=false) {
    const name = document.getElementById('sessionName').value.trim();
    const color = document.getElementById('sessionColor').value;
    const date = {};
    console.log(selectedDates)
    if (select){
        Object.entries(selectedDates).forEach(([tgl, id]) =>{
            if(!date[id]){
                date[id] = [];
            }
            date[id].push(tgl);
        })
    }
    if (name) {
        fetch('/calendar', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                name : name,
                colour : color,
                tanggal : date
            })
        }).then(response => response.json())
        .then(data => {
            if(data.success){
                initCalendar();
                if(data.save){
                    window.location.reload()
                }else{
                    return;
                }
            }
            alert(data.message);
        })

        cancelSessionForm();
    }
}

function deleteSession(id) {
    Object.keys(selectedDates).forEach(key => {
        if (selectedDates[key] === id) {
            delete selectedDates[key];
        }
    });
    if (sessions.length > 0) {
        fetch(`/delete-session/${id}`)
        .then(response => response.json())
        .then(data => {
            if(data.success){
                initCalendar();
            }
            alert(data.message);
        })
    }
}

function selectSession(id) {
    currentSessionId = id;
    initCalendar();
}

function toggleDate(day) {
    console.log(selectedDates)
    const dateString = `${waktutertentu.getFullYear()}-${waktutertentu.getMonth()}-${("0" + day).slice(-2)}`;
    if (selectedDates[dateString] === currentSessionId) {
        if (Object.values(selectedDates).filter(value => value === currentSessionId).length < 2){
            alert("You can't change this without choose another date");
            return;
        }
        delete selectedDates[dateString];
    } else {
        selectedDates[dateString] = currentSessionId;
    }
    saveSession(true);
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