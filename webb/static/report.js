// State management
let currentDate = new Date();
let selectedDate = new Date();
let dailyReportChart, studyReportChart;

// Initialize data store for different dates
const dateData = new Map();

// Helper function to format date key
function getDateKey(date) {
    return date.toISOString().split('T')[0];
}

var tasks = []

async function fetchTasks(date = null) {
    url = '/tasks'
    if (date) {
        url += '?date=' + date
    }
    tempt = null
    await fetch(url)
        .then(response => response.json())
        .then(data => {
            console.log('Fetched tasks:', data); // Debug
            tasks = data.tasks; // Simpan daftar tugas
            tempt = data.tasks
        })
        .catch(error => {
            console.error('Error fetching tasks:', error);
            alert('Failed to load tasks');
        });

    return tempt
}

// Helper function to generate random data for new dates
async function getData(dateKey) {

    const dt = await fetchTasks(dateKey)

    // categoryze to every labels based on dt['description']
    dts = {
        others: 0,
        pjct: 0,
        stdy: 0,
        exercise: 0
    }
    dt.forEach((task) => {
        console.log(task.description.toLowerCase())
        switch (task.description.toLowerCase()) {
            case 'project group':
                dts.pjct += task.duration;
                break;
            case 'study':
                dts.stdy += task.duration;
                break;
            case 'exercise':
                dts.exercise += task.duration;
                break;
            default:
                dts.others += task.duration;
        }
    })

    ret = {
        daily: {
            others: dts.others,
            projectGroup: dts.pjct,
            study: dts.stdy,
            exercise: dts.exercise
        },
        study: dts.stdy / 60
    }

    return ret;
}

// Time update function
function updateTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    // document.getElementById('time').textContent = `${hours} : ${minutes} : ${seconds}`;
}

// Date display update function
function updateDateDisplay() {
    const days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat'];
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    
    const isToday = selectedDate.toDateString() === new Date().toDateString();
    const day = days[selectedDate.getDay()];
    const month = months[selectedDate.getMonth()];
    const date = selectedDate.getDate();
    
    const displayText = isToday ? 
        `Today . ${day}` : 
        `${month} ${date} . ${day}`;
    
    document.getElementById('date').textContent = displayText;

    // Handle next day button state
    const nextBtn = document.getElementById('nextDay');
    if (selectedDate.toDateString() === new Date().toDateString()) {
        nextBtn.classList.add('disabled');
    } else {
        nextBtn.classList.remove('disabled');
    }
}

// Chart update functions
async function updateDailyChart(dt = null) {
    d = dt ? dt : selectedDate

    // console.log(d)
    const dateKey = getDateKey(d);
    // if (!dateData.has(dateKey)) {
    // }
    // dateData.set(dateKey, await getData(dateKey));

    for (i = 1; i <= 4; i++) {
        dt_ = new Date()
        dt_.setDate(selectedDate.getDate() - 1 * i)
        dateData.set(dateKey, await getData(dateKey));
    }

    updateStudyChart()
    const data = dateData.get(dateKey);

    const chartData = {
        labels: ['Others', 'Project Group', 'Study', 'Exercise'],
        datasets: [{
            data: [
                data.daily.others || 0,
                data.daily.project || 0,
                data.daily.study || 0,
                data.daily.exercise || 0
            ],
            backgroundColor: ['#4A4A8A', '#6A6AB8', '#8A8AD8', '#AAAAF8'],
            borderColor: '#1E2A38',
            borderWidth: 1
        }]
    };

    if (dailyReportChart) {
        dailyReportChart.data = chartData;
        dailyReportChart.update();
    } else {
        const ctx = document.getElementById('dailyReportChart').getContext('2d');
        dailyReportChart = new Chart(ctx, {
            type: 'doughnut',
            data: chartData,
            options: {
                responsive: true,
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

async function updateStudyChart() {
    const labels = [];
    const data = [];
    
    // Get data for the last 4 days
    for (let i = 0; i < 4; i++) {
        const date = new Date(selectedDate);
        date.setDate(date.getDate() - i);
        const dateKey = getDateKey(date);
        
        if (!dateData.has(dateKey)) {
            dateData.set(dateKey, await getData(dateKey));
        }
        
        const dayData = dateData.get(dateKey);
        data.unshift(dayData.study);
        
        if (i === 0) {
            labels.unshift('Today');
        } else {
            const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
            labels.unshift(days[date.getDay()]);
        }
    }

    const chartData = {
        labels: labels,
        datasets: [{
            label: 'Study Hours',
            data: data,
            backgroundColor: '#8A8AD8',
            borderColor: '#1E2A38',
            borderWidth: 1
        }]
    };

    if (studyReportChart) {
        studyReportChart.data = chartData;
        studyReportChart.update();
    } else {
        const ctx = document.getElementById('studyReportChart').getContext('2d');
        studyReportChart = new Chart(ctx, {
            type: 'bar',
            data: chartData,
            options: {
                responsive: true,
                scales: {
                    y: {
                        beginAtZero: true,
                        max: 10,
                        grid: {
                            color: '#374151'
                        },
                        ticks: {
                            color: '#FFFFFF'
                        }
                    },
                    x: {
                        grid: {
                            display: false
                        },
                        ticks: {
                            color: '#FFFFFF'
                        }
                    }
                },
                plugins: {
                    legend: {
                        display: false
                    }
                }
            }
        });
    }
}

// Navigation handlers
document.getElementById('prevDay').addEventListener('click', async () => {
    selectedDate.setDate(selectedDate.getDate() - 1);
    updateDateDisplay();
    await updateDailyChart();
    // updateStudyChart();
});

document.getElementById('nextDay').addEventListener('click', async () => {
    if (selectedDate.toDateString() !== new Date().toDateString()) {
        selectedDate.setDate(selectedDate.getDate() + 1);
        updateDateDisplay();
        await updateDailyChart();
        // updateStudyChart();
    }
});

// Initial setup
setInterval(updateTime, 1000);
updateDateDisplay();
updateDailyChart()
// for (i = 1; i <= 4; i++) {
//     dt_ = new Date()
//     dt_.setDate(selectedDate.getDate() - 1 * i)
//     updateDailyChart(dt_);
// }
// updateStudyChart();