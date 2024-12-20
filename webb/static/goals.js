
class GoalsTracker {
    constructor() {
        this.goals = [];
        this.isAddingGoal = false;
        this.init();
        this.startTimeoutChecker();
    }

    init() {
        this.addGoalBtn = document.getElementById('addGoalBtn');
        this.tableBody = document.getElementById('goalsTableBody');
        this.notification = document.getElementById('notification');
        this.notificationMessage = document.getElementById('notificationMessage');
                
        this.addGoalBtn.addEventListener('click', () => this.showAddGoalForm());
        this.loadGoals();
        this.renderGoals();
    }

    startTimeoutChecker() {
    // Check for timeouts every minute
        setInterval(() => this.checkTimeouts(), 60000);
        // Initial check
            this.checkTimeouts();
    }

    checkTimeouts() {
        const now = new Date();
        let hasChanges = false;

        this.goals.forEach(goal => {
            if (goal.timeToAchieve && goal.status !== 'Time Out') {
                const deadline = new Date(goal.timeToAchieve);
                    if (now > deadline) {
                        goal.status = 'Time Out';
                        hasChanges = true;
                        this.showNotification(`Your goal "${goal.goal}" has timed out!`);
                    }
            }
        });

            if (hasChanges) {
                this.saveGoals();
                this.renderGoals();
            }
    }

    showNotification(message) {
        this.notificationMessage.textContent = message;
        this.notification.classList.add('show');
        setTimeout(() => {
            this.notification.classList.remove('show');
        }, 5000);
    }

    loadGoals() {
        const savedGoals = localStorage.getItem('goals');
        if (savedGoals) {
            this.goals = JSON.parse(savedGoals);
        }
    }

    saveGoals() {
        localStorage.setItem('goals', JSON.stringify(this.goals));
    }

    renderGoals() {
        this.tableBody.innerHTML = '';
        this.goals.forEach((goal, index) => {
        const row = this.createGoalRow(goal);
        this.tableBody.appendChild(row);
        });
    }

    createGoalRow(goal) {
        const row = document.createElement('tr');
                
        // Goal input
        const goalTd = document.createElement('td');
        const goalInput = document.createElement('input');
        goalInput.type = 'text';
        goalInput.value = goal.goal;
        goalInput.className = 'editable';
        goalInput.addEventListener('change', (e) => {
            goal.goal = e.target.value;
            this.saveGoals();
        });
        goalTd.appendChild(goalInput);
                
        // Session input
        const sessionTd = document.createElement('td');
        const sessionInput = document.createElement('input');
        sessionInput.type = 'text';
        sessionInput.value = goal.session;
        sessionInput.className = 'editable';
        sessionInput.addEventListener('change', (e) => {
            goal.session = e.target.value;
            this.saveGoals();
        });
        sessionTd.appendChild(sessionInput);
                
        // Status input
        const statusTd = document.createElement('td');
        const statusInput = document.createElement('input');
        statusInput.type = 'text';
        statusInput.value = goal.status || 'Pending';
        statusInput.className = `editable ${goal.status === 'Time Out' ? 'status-timeout' : 'status-pending'}`;
        statusInput.readOnly = goal.status === 'Time Out';
        statusInput.addEventListener('change', (e) => {
            goal.status = e.target.value;
            this.saveGoals();
        });
        statusTd.appendChild(statusInput);
                
        // Time to Achieve input
        const timeTd = document.createElement('td');
        const timeInput = document.createElement('input');
        timeInput.type = 'datetime-local';
        timeInput.value = goal.timeToAchieve ? goal.timeToAchieve.slice(0, 16) : '';
        timeInput.className = 'editable';
        timeInput.addEventListener('change', (e) => {
            goal.timeToAchieve = e.target.value;
            this.saveGoals();
            this.checkTimeouts();
        });
        timeTd.appendChild(timeInput);

        // Delete button
        const actionsTd = document.createElement('td');
        const deleteBtn = document.createElement('button');
        deleteBtn.className = 'btn btn-ghost';
        deleteBtn.innerHTML = `
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <path d="M18 6 6 18M6 6l12 12"/>
        </svg>
        `;
        deleteBtn.addEventListener('click', () => {
            this.deleteGoal(goal.id);
        });
        actionsTd.appendChild(deleteBtn);

        row.appendChild(goalTd);
        row.appendChild(sessionTd);
        row.appendChild(statusTd);
        row.appendChild(timeTd);
        row.appendChild(actionsTd);

        return row;
        }

        showAddGoalForm() {
            if (this.isAddingGoal) return;

            this.isAddingGoal = true;
            const row = document.createElement('tr');
            row.className = 'new-goal-row';
                
            const goalTd = document.createElement('td');
            const goalInput = document.createElement('input');
            goalInput.type = 'text';
            goalInput.className = 'editable';
            goalInput.placeholder = 'Enter your goal';
            goalTd.appendChild(goalInput);

            const sessionTd = document.createElement('td');
            const sessionInput = document.createElement('input');
            sessionInput.type = 'text';
            sessionInput.className = 'editable';
            sessionInput.placeholder = 'Enter session';
            sessionTd.appendChild(sessionInput);

            const timeTd = document.createElement('td');
            const timeInput = document.createElement('input');
            timeInput.type = 'datetime-local';
            timeInput.className = 'editable';
            timeTd.appendChild(timeInput);
                
            const actions = document.createElement('td');
            actions.colSpan = "2";
                
            const saveBtn = document.createElement('button');
            saveBtn.className = 'btn btn-ghost btn-save';
            saveBtn.textContent = 'Save';
                
            const cancelBtn = document.createElement('button');
            cancelBtn.className = 'btn btn-ghost btn-cancel';
            cancelBtn.textContent = 'Cancel';
                
            actions.appendChild(saveBtn);
            actions.appendChild(cancelBtn);
                
            row.appendChild(goalTd);
            row.appendChild(sessionTd);
            row.appendChild(document.createElement('td')); // Empty status cell
            row.appendChild(timeTd);
            row.appendChild(actions);
                
            this.tableBody.insertBefore(row, this.tableBody.firstChild);
            goalInput.focus();

            saveBtn.addEventListener('click', () => {
                this.addGoal(goalInput.value, sessionInput.value, timeInput.value);
            });

            cancelBtn.addEventListener('click', () => {
                row.remove();
                this.isAddingGoal = false;
            });

            goalInput.addEventListener('keypress', (e) => {
                if (e.key === 'Enter') {
                    this.addGoal(goalInput.value, sessionInput.value, timeInput.value);
                }
            });
        }

        addGoal(goalText, sessionText, timeText) {
            if (!goalText.trim()) return;

            const newGoal = {
                id: Date.now(),
                goal: goalText,
                session: sessionText,
                status: 'Pending',
                timeToAchieve: timeText
            };

            fetch('/savegoals', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    goalss : goalText,
                    session : sessionText,
                    timeachieve : timeText,
                })
            })


            this.goals.unshift(newGoal);
            this.saveGoals();
            this.renderGoals();
            this.isAddingGoal = false;
        }

        deleteGoal(id) {
            this.goals = this.goals.filter(goal => goal.id !== id);
            this.saveGoals();
            this.renderGoals();
        }
    }

        // Initialize the application
    document.addEventListener('DOMContentLoaded', () => {
        new GoalsTracker();
    });