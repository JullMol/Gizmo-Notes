from flask import Flask, render_template, Blueprint, jsonify, request
from .database import ToDoListD, ToDoListA, ToDoListE, db
from datetime import datetime
from flask_login import login_required, current_user

todo = Blueprint('todo', __name__)
# Global lists untuk menyimpan tugas
day_tasks = []
assignment_tasks = []
event_tasks = []

@todo.route('/save_day_task', methods=['POST'])
@login_required
def save_day_task():
    data = request.get_json()
    required_fields = ['date', 'time', 'placement', 'activities', 'priority']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"status": "error", "message": f"'{field}' is required"}), 400
        
    time = data['time']
    if len(time.split(':')) == 2:  # Format HH:MM
            time += ':00'
    
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time = datetime.strptime(time, '%H:%M:%S').time()

    new_task = ToDoListD(user_id=current_user.id, date=date, time=time, placement=data['placement'], activities=data['activities'], priority=data['priority'])
    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task saved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error saving task', 'error': str(e)}), 500
    
    # # day_tasks.append(data)
    # print(f"Day Task: {day_tasks}")
    # return jsonify({"status": "success", "task_id": new_task.id})

@todo.route('/save_assignment_task', methods=['POST'])
@login_required
def save_assignment_task():
    data = request.get_json()
    required_fields = ['date', 'time', 'subject', 'details', 'priority']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"status": "error", "message": f"'{field}' is required"}), 400
        
    time = data['time']
    if len(time.split(':')) == 2:  # Format HH:MM
            time += ':00'
    
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time = datetime.strptime(time, '%H:%M:%S').time()

    new_task = ToDoListA(user_id=current_user.id, date=date, time=time, subject=data['subject'], details=data['details'], priority=data['priority'])
    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task saved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error saving task', 'error': str(e)}), 500
    
    # assignment_tasks.append(data)
    # print(f"Assignment Task: {assignment_tasks}")
    # return jsonify({"status": "success", "task_id": new_task.id})

@todo.route('/save_event_task', methods=['POST'])
@login_required
def save_event_task():
    data = request.get_json()
    required_fields = ['date', 'time', 'location', 'details', 'priority']
    for field in required_fields:
        if not data.get(field):
            return jsonify({"status": "error", "message": f"'{field}' is required"}), 400
        
    time = data['time']
    if len(time.split(':')) == 2:  # Format HH:MM
            time += ':00'
    
    date = datetime.strptime(data['date'], '%Y-%m-%d').date()
    time = datetime.strptime(time, '%H:%M:%S').time()

    new_task = ToDoListE(user_id=current_user.id, date=date, time=time, location=data['location'], details=data['details'], priority=data['priority'])
    try:
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task saved successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error saving task', 'error': str(e)}), 500
    
    # event_tasks.append(data)
    # print(f"Event Task: {event_tasks}")
    # return jsonify({"status": "success", "tasks": event_tasks})

@todo.route('/get_day_tasks', methods=['GET', 'DELETE'])
@login_required
def day_tasks():
    if request.method == 'GET':
        # Logika untuk mendapatkan data
        try:
            tasks = ToDoListD.query.filter_by(user_id=current_user.id).all()
            task_list = [{
                'id': task.id,
                'date': task.date.strftime('%Y-%m-%d'),
                'time': task.time.strftime('%H:%M'),
                'placement': task.placement,
                'activities': task.activities,
                'priority': task.priority
            } for task in tasks]
            return jsonify(task_list), 200
        except Exception as e:
            return jsonify({'message': 'Error retrieving tasks', 'error': str(e)}), 500

    elif request.method == 'DELETE':
        # Logika untuk menghapus data
        task_id = request.args.get('id')  # ID tugas dikirim melalui query parameter
        if not task_id:
            return jsonify({'message': 'Task ID is required'}), 400
        try:
            task = ToDoListD.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()
                return jsonify({'message': 'Task deleted successfully'}), 200
            else:
                return jsonify({'message': 'Task not found'}), 404
        except Exception as e:
            return jsonify({'message': 'Error deleting task', 'error': str(e)}), 500

@todo.route('/get_assignment_tasks', methods=['GET', 'DELETE'])
@login_required
def get_assignment_tasks():
    if request.method == 'GET':
        try:
            tasks = ToDoListA.query.filter_by(user_id=current_user.id).all()
            task_list = [{
                'id': task.id,
                'date': task.date.strftime('%Y-%m-%d'),
                'time': task.time.strftime('%H:%M'),
                'subject': task.subject,
                'details': task.details,
                'priority': task.priority
            } for task in tasks]
            return jsonify(task_list), 200
        except Exception as e:
            return jsonify({'message': 'Error retrieving tasks', 'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        # Logika untuk menghapus data
        task_id = request.args.get('id')  # ID tugas dikirim melalui query parameter
        if not task_id:
            return jsonify({'message': 'Task ID is required'}), 400
        try:
            task = ToDoListA.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()
                return jsonify({'message': 'Task deleted successfully'}), 200
            else:
                return jsonify({'message': 'Task not found'}), 404
        except Exception as e:
            return jsonify({'message': 'Error deleting task', 'error': str(e)}), 500

@todo.route('/get_event_tasks', methods=['GET', 'DELETE'])
@login_required
def get_event_tasks():
    if request.method == 'GET':
        try:
            tasks = ToDoListE.query.filter_by(user_id=current_user.id).all()
            task_list = [{
                'id': task.id,
                'date': task.date.strftime('%Y-%m-%d'),
                'time': task.time.strftime('%H:%M'),
                'location': task.location,
                'details': task.details,
                'priority': task.priority
            } for task in tasks]
            return jsonify(task_list), 200
        except Exception as e:
            return jsonify({'message': 'Error retrieving tasks', 'error': str(e)}), 500
    
    elif request.method == 'DELETE':
        # Logika untuk menghapus data
        task_id = request.args.get('id')  # ID tugas dikirim melalui query parameter
        if not task_id:
            return jsonify({'message': 'Task ID is required'}), 400
        try:
            task = ToDoListE.query.get(task_id)
            if task:
                db.session.delete(task)
                db.session.commit()
                return jsonify({'message': 'Task deleted successfully'}), 200
            else:
                return jsonify({'message': 'Task not found'}), 404
        except Exception as e:
            return jsonify({'message': 'Error deleting task', 'error': str(e)}), 500

if __name__ == '__main__':
    todo.run(debug=True)