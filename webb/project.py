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
    
    # Parsing waktu dari request
    tm = data.get('timeCreated')
    tm1 = data.get('timeFinished')
    
    try:
        tm_ = datetime.strptime(tm, '%Y-%m-%dT%H:%M')  # Format input dari frontend
        tm1_ = datetime.strptime(tm1, '%Y-%m-%dT%H:%M')
    except ValueError as e:
        return jsonify({'status': 'error', 'message': str(e)}), 400

    # Menyimpan data ke database
    project_table = pproject(
        user_id=current_user.id,
        project_name=data.get('projekname'),
        session2=data.get('session2'),
        time_created=tm_,
        time_finished=tm1_,
    )
    db.session.add(project_table)
    db.session.commit()

    return jsonify({'status': 'success', 'message': 'Project added successfully'}), 200

@project.route('/getproject', methods=['GET'])
@login_required
def getproject():
<<<<<<< HEAD
    tasks_ = pproject.query.all()  # Ambil semua data project
=======
    tasks_ = pproject.query.filter_by(user_id=current_user.id).all()  # Fetch all projects
>>>>>>> 64e6e916d1ebdfb2f558ba1651dcba27f4e7ddd8
    res = []

    # Format setiap project ke dalam JSON
    for task in tasks_:
        # Gunakan `.isoformat()` untuk mendapatkan format ISO8601
        res.append({
            'id': task.id,
            'project_name': task.project_name,
            'session2': task.session2,
            'start': task.time_created.isoformat(),  # Format ISO8601
            'end': task.time_finished.isoformat()   # Format ISO8601
        })

    return jsonify({'status': 'success', 'tasks': res}), 200

if __name__ == '__main__':
    project.run(debug=True)