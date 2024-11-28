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

// Helper function to generate random data for new dates
function generateRandomData() {
    return {
        daily: {
            others: 50 + Math.random() * 20,
            projectGroup: 15 + Math.random() * 10,
            study: 10 + Math.random() * 10,
            exercise: 3 + Math.random() * 5
        },
        study: Math.floor(Math.random() * 8) + 2 // 2-10 hours
    };
}

// Time update function
function updateTime() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    const seconds = String(now.getSeconds()).padStart(2, '0');
    document.getElementById('time').textContent = `${hours} : ${minutes} : ${seconds}`;
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
function updateDailyChart() {
    const dateKey = getDateKey(selectedDate);
    if (!dateData.has(dateKey)) {
        dateData.set(dateKey, generateRandomData());
    }
    const data = dateData.get(dateKey);

    const chartData = {
        labels: ['Others', 'Project Group', 'Study', 'Exercise'],
        datasets: [{
            data: [
                data.daily.others,
                data.daily.projectGroup,
                data.daily.study,
                data.daily.exercise
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

function updateStudyChart() {
    const labels = [];
    const data = [];
    
    // Get data for the last 4 days
    for (let i = 0; i < 4; i++) {
        const date = new Date(selectedDate);
        date.setDate(date.getDate() - i);
        const dateKey = getDateKey(date);
        
        if (!dateData.has(dateKey)) {
            dateData.set(dateKey, generateRandomData());
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
document.getElementById('prevDay').addEventListener('click', () => {
    selectedDate.setDate(selectedDate.getDate() - 1);
    updateDateDisplay();
    updateDailyChart();
    updateStudyChart();
});

document.getElementById('nextDay').addEventListener('click', () => {
    if (selectedDate.toDateString() !== new Date().toDateString()) {
        selectedDate.setDate(selectedDate.getDate() + 1);
        updateDateDisplay();
        updateDailyChart();
        updateStudyChart();
    }
});

// Initial setup
setInterval(updateTime, 1000);
updateDateDisplay();
updateDailyChart();
updateStudyChart();