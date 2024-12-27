from flask import  Flask , render_template, request, redirect, url_for, Blueprint, jsonify
from .database import db, pproject
from datetime import datetime
from flask_login import login_required, current_user

project = Blueprint("project", __name__)

project_list = []

@project.route('/saveproject', methods=['POST'])
@login_required
def Saveproject():
    data = request.get_json()
    tm = data.get('timeCreated')
    tm_ = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
    tm1 = data.get('timeFinished')
    tm1_ = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
    project_table = pproject(
        user_id=current_user.id,
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
@login_required
def getproject():
    tasks_ = pproject.query.filter_by(user_id=current_user.id).all()  # Fetch all projects
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