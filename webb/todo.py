from flask import Flask, render_template, Blueprint, jsonify, request

todo = Blueprint('todo', __name__)
# Global lists untuk menyimpan tugas
day_tasks = []
assignment_tasks = []
event_tasks = []

@todo.route('/')
def index():
    return render_template('home.html')

@todo.route('/home.html')
def menu():
    return render_template('home.html')

@todo.route('/search.html')
def search():
    return render_template('search.html')

@todo.route('/timer.html')
def pomo():
    return render_template('timer.html')

@todo.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@todo.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@todo.route('/Day.html')
def Day():
    return render_template('Day.html')

@todo.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@todo.route('/Event.html')
def Event():
    return render_template('Event.html')

@todo.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@todo.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@todo.route('/Group.html')
def Group():
    return render_template('Group.html')

@todo.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@todo.route('/Invite.html')
def invite():
    return render_template('Invite.html')

@todo.route('/save_day_task', methods=['POST'])
def save_day_task():
    data = request.get_json()
    day_tasks.append(data)
    print(f"Day Task: {day_tasks}")
    return jsonify({"status": "success", "tasks": day_tasks})

@todo.route('/save_assignment_task', methods=['POST'])
def save_assignment_task():
    data = request.get_json()
    assignment_tasks.append(data)

    # save disini

    print(f"Assignment Task: {assignment_tasks}")
    return jsonify({"status": "success", "tasks": assignment_tasks})

@todo.route('/save_event_task', methods=['POST'])
def save_event_task():
    data = request.get_json()
    event_tasks.append(data)
    print(f"Event Task: {event_tasks}")
    return jsonify({"status": "success", "tasks": event_tasks})

@todo.route('/get_day_tasks')
def get_day_tasks():
    return jsonify(day_tasks)

@todo.route('/get_assignment_tasks')
def get_assignment_tasks():
    return jsonify(assignment_tasks)

@todo.route('/get_event_tasks')
def get_event_tasks():
    return jsonify(event_tasks)

if __name__ == '__main__':
    todo.run(debug=True)