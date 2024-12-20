from flask import Flask, request, render_template, Blueprint, jsonify
from datetime import datetime, timedelta
import time
from .database import Timer, db, GGoals

timer = Blueprint('timer', __name__)

tasks = []
tasks_by_date = {}
goals_by_date = {}
current_task_index = None

@timer.route('/')
def index():
    return render_template('home.html')

@timer.route('/home.html')
def home():
    return render_template('home.html')

@timer.route('/search.html')
def search():
    return render_template('search.html')

@timer.route('/timer.html')
def pomo():
    return render_template('timer.html')

@timer.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@timer.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@timer.route('/Day.html')
def Day():
    return render_template('Day.html')

@timer.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@timer.route('/Event.html')
def Event():
    return render_template('Event.html')

@timer.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@timer.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@timer.route('/Group.html')
def Group():
    return render_template('Group.html')

@timer.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@timer.route('/Project.html')
def Project():
    return render_template('Project.html')

@timer.route('/Invite.html')
def invite():
    return render_template('Invite.html')

@timer.route('/page-goals')
def page_goals():
    return render_template('Goals.html')

@timer.route('/add-task', methods=['POST'])
def add_task():
    try:
        data = request.get_json()
        print("Received data:", data)  # Debug print
        
        task_description = data.get('taskDescription')
        start_time_str = data.get('startTime')
        end_time_str = data.get('endTime')
        date = data.get('date')
        status = data.get('status')
        
        print(f"Task: {task_description}")  # Debug print
        print(f"Start time: {start_time_str}")  # Debug print
        print(f"End time: {end_time_str}")  # Debug print
        print(f"Date Time: {date}")
        
        if not all([task_description, start_time_str, end_time_str, date]):
            return jsonify({
                'status': 'error',
                'message': 'Missing required fields'
            }), 400

        try:
            # Parse times and calculate duration
            start_time = datetime.strptime(start_time_str, '%I:%M %p').time()
            end_time = datetime.strptime(end_time_str, '%I:%M %p').time()
            
            # Validasi apakah waktu overlap
            if is_time_overlap(start_time, end_time, tasks):
                return jsonify({
                    'status': 'error',
                    'message': 'Time overlaps with an existing task or break time.'
                }), 400
            
            # Convert times to minutes since midnight
            start_minutes = start_time.hour * 60 + start_time.minute
            end_minutes = end_time.hour * 60 + end_time.minute
            
            # Calculate duration
            duration = end_minutes - start_minutes
            
            # If duration is negative, assume it spans midnight
            if duration < 0:
                duration += 24 * 60  # Add 24 hours in minutes
            
            print(f"Calculated duration: {duration} minutes")  # Debug print
            new_data = Timer(task=task_description, date=datetime.strptime(date, "%Y-%m-%d").date(), start_time=start_time, end_time=end_time, duration=duration, status= 'pending')
            db.session.add(new_data)
            db.session.commit()
            
            # Store task
            task = {
                'id': new_data.id,
                'description': task_description,
                'startTime': start_time_str,
                'endTime': end_time_str,
                'date': date,
                'duration': duration,
            }
            # tasks.append(task)
            
            # if date not in tasks_by_date:
            #     tasks_by_date[date] = []
            # tasks_by_date[date].append(task)
            # print(f"Task added for {date}: {task}")
            return jsonify({'status': 'success', 'message': 'Task added successfully', 'task': task}), 200

            # return jsonify({
            #     'status': 'success',
            #     'duration': duration,
            #     'message': 'Task added successfully'
            # })

        except ValueError as e:
            print(f"Time parsing error: {str(e)}")  # Debug print
            return jsonify({
                'status': 'error',
                'message': f'Invalid time format: {str(e)}'
            }), 400

    except Exception as e:
        print(f"Server error: {str(e)}")  # Debug print
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500

# Endpoint untuk memulai timer untuk tugas tertentu
@timer.route('/start-task/<int:task_id>', methods=['POST'])
def start_task(task_id):
    global current_task_index
    try:
        sum_timer = Timer.query.count()
        if task_id < 0 and task_id >= sum_timer:
            return jsonify({
                'status': 'error',
                'message': 'Invalid task ID'
            }), 400
            
        # if current_task_index is not None:
        #     tasks[current_task_index]['status'] = 'completed'
        task = Timer.query.filter_by(id=task_id).first()
        # task = tasked
        task.status = 'running'
        db.session.commit()
        current_task_index = task_id

        return jsonify({
            'status': 'success',
            'duration': task.duration,
            'message': f'Timer started for task: {task.task}'
        })

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f'Server error: {str(e)}'
        }), 500
        
@timer.route('/data-by-date/<string:date>', methods=['GET'])
def get_data_by_date(date):
    try:
        # Validasi format tanggal
        datetime.strptime(date, '%Y-%m-%d')

        # Ambil tugas berdasarkan tanggal
        tasks = Timer.query.filter_by(date=datetime.strptime(date, "%Y-%m-%d").date()).all()
        result = [
            {
                'id': task.id,
                'description': task.task,
                'startTime': task.start_time.strftime('%I:%M %p'),
                'endTime': task.end_time.strftime('%I:%M %p'),
                'date': task.date.strftime('%Y-%m-%d'),
                'duration': task.duration,
                'startable': task.status != 'running'
            }
            for task in tasks
        ]
        return jsonify({'status': 'success', 'tasks': result}), 200

    except ValueError:
        return jsonify({'status': 'error', 'message': 'Invalid date format'}), 400
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@timer.route('/tasks', methods=['GET'])
def get_tasks():
    print("Tasks defined")
    try:
        # Ambil parameter tanggal (jika ada)
        date = request.args.get('date')
        print(date)
        if date:
            tasks = Timer.query.filter_by(date=datetime.strptime(date, "%Y-%m-%d").date()).all()
        else:
            # Gabungkan semua task jika tidak ada tanggal yang diberikan
            # tasks = [task for tasks in tasks_by_date.values() for task in tasks]
            tasks = Timer.query.all()

        # Tambahkan atribut `startable`
        # result = [
        #     {**task.__dict__, 'startable': task.status != 'running'}
        #     for task in tasks
        #     if not task.__dict__.get('_sa_instance_state')  # Hilangkan atribut internal SQLAlchemy
        # ]
        result = [
            {
                'id': task.id,
                'description': task.task,
                'startTime': task.start_time.strftime('%I:%M %p'),
                'endTime': task.end_time.strftime('%I:%M %p'),
                'date': task.date.strftime('%Y-%m-%d'),
                'duration': task.duration,
                'startable': task.status != 'running'
            }
            for task in tasks
        ]

        print(result)

        return jsonify({'status': 'success', 'tasks': result}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@timer.route('/all-data', methods=['GET'])
def get_all_data():
    try:
        all_data = {
            'tasks': [
                {'date': date, 'tasks': tasks}
                for date, tasks in tasks_by_date.items()
            ],
            'goals': [
                {'date': date, 'goals': goals}
                for date, goals in goals_by_date.items()
            ]
        }

        return jsonify({'status': 'success', 'data': all_data}), 200

    except Exception as e:
        print(f"Error fetching all data: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500

# Fungsi tambahan
def is_time_overlap(new_start, new_end, tasks):
    """
    Cek apakah rentang waktu baru overlap dengan tugas atau waktu break.
    """
    new_start_minutes = new_start.hour * 60 + new_start.minute
    new_end_minutes = new_end.hour * 60 + new_end.minute

    # Sesuaikan jika melewati tengah malam
    if new_end_minutes < new_start_minutes:
        new_end_minutes += 24 * 60

    for task in tasks:
        existing_start = datetime.strptime(task['startTime'], '%I:%M %p')
        existing_end = datetime.strptime(task['endTime'], '%I:%M %p')
        
        existing_start_minutes = existing_start.hour * 60 + existing_start.minute
        existing_end_minutes = existing_end.hour * 60 + existing_end.minute

        # Sesuaikan jika melewati tengah malam
        if existing_end_minutes < existing_start_minutes:
            existing_end_minutes += 24 * 60

        # Tambahkan waktu istirahat 5 menit setelah tugas selesai
        existing_end_minutes += 5

        # Cek overlap dengan perhitungan menit
        if (new_start_minutes < existing_end_minutes and 
            new_end_minutes > existing_start_minutes):
            return True
    return False

def calculate_duration(start_time, end_time):
    """
    Hitung durasi tugas dalam menit.
    """
    start_minutes = start_time.hour * 60 + start_time.minute
    end_minutes = end_time.hour * 60 + end_time.minute
    
    # Jika durasi negatif, artinya melewati tengah malam
    duration = end_minutes - start_minutes
    if duration < 0:
        duration += 24 * 60  # Tambahkan 24 jam dalam menit

    return duration

@timer.route('/notifications/<string:date>', methods=['GET'])
def get_notifications(date):
    try:
        tasks = tasks_by_date.get(date, [])
        notifications = []

        for task in tasks:
            start_time = datetime.strptime(task['startTime'], '%I:%M %p')
            end_time = datetime.strptime(task['endTime'], '%I:%M %p')

            notifications.append({
                "type": "start",
                "time": start_time.strftime('%H:%M:%p'),
                "message": f"Task '{task['description']}' is starting!"
            })

            notifications.append({
                "type": "end",
                "time": end_time.strftime('%H:%M:%p'),
                "message": f"Task '{task['description']}' has ended!"
            })

            # Tambahkan waktu istirahat (misal, 5 menit setelah selesai)
            break_start_time = end_time + timedelta(minutes=5)
            break_end_time = break_start_time + timedelta(minutes=5)
            notifications.append({
                "type": "break_start",
                "time": break_start_time.strftime('%H:%M:%p'),
                "message": "Break time has started!"
            })
            notifications.append({
                "type": "break_end",
                "time": break_end_time.strftime('%H:%M:%p'),
                "message": "Break time has ended!"
            })

        return jsonify({'status': 'success', 'notifications': notifications}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@timer.route('/reset-task', methods=['POST'])
def reset_task():
    global tasks, current_task_index
    if current_task_index is not None:
        task = Timer.query.filter_by(id=current_task_index).first()
        # tasks[current_task_index]['status'] = 'completed'
        current_task_index = None
    
    return jsonify({
        'status': 'success',
        'message': 'Timer reset'
    })

if __name__ == '__main__':
    timer.run(debug=True)