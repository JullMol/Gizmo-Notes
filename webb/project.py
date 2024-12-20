from flask import  Flask , render_template, request, redirect, url_for, Blueprint, jsonify
from .database import db, pproject
from datetime import datetime

project = Blueprint("project", __name__)

project_list = []


@project.route('/')
def index():
    return render_template('home.html')

@project.route('/home.html')
def menu():
    return render_template('home.html')

@project.route('/search.html')
def search():
    return render_template('search.html')

@project.route('/timer.html')
def pomo():
    return render_template('timer.html')

@project.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@project.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@project.route('/Day.html')
def Day():
    return render_template('Day.html')

@project.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@project.route('/Event.html')
def Event():
    return render_template('Event.html')

@project.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@project.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@project.route('/Group.html')
def Group():
    return render_template('Group.html')

@project.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@project.route('/Invite.html')
def invite():
    return render_template('Invite.html')

@project.route('/saveproject', methods=['POST'])
def Saveproject():
    data = request.get_json()
    tm = data.get('timeCreated')
    tm_ = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
    tm1 = data.get('timeFinished')
    tm1_ = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
    project_table = pproject(
        project_name=data.get('projekname'),
        session2=data.get('session2'),
        time_created=tm_,
        time_finished=tm1_,
    )
    db.session.add(project_table)
    db.session.commit()

    # print(f"Task added for {date}: {task}")
    return jsonify({'status': 'success', 'message': 'Task added successfully'}), 200

@project.route('/getproject', methods=['GET'])
def getproject():
    tasks_ = pproject.query.all()  # Fetch all projects
    res = []

    # Loop through each task and manually format the time fields
    for task in tasks_:
        # Convert datetime objects to string in the desired format
        start = task.time_created.strftime('%Y-%m-%dT%H:%M:%S')  # Format the datetime
        end = task.time_finished.strftime('%Y-%m-%dT%H:%M:%S')  # Format the datetime
        
        # Append the task data along with formatted times
        res.append({
            'id': task.id,
            'project_name': task.project_name,
            'session2': task.session2,
            'time_created': start,
            'time_finished': end
        })

    return jsonify({'status': 'success', 'tasks': res}), 200

if __name__ == '__main__':
    project.run(debug=True)