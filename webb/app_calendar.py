from flask import Flask, render_template, Blueprint, jsonify, request
from .database import db, ccalendar
from datetime import datetime
calendar = Blueprint('calendar', __name__)

# calendar = []

@calendar.route('/')
def index():
    return render_template('home.html')

@calendar.route('/home.html')
def menu():
    return render_template('home.html')

@calendar.route('/search.html')
def search():
    return render_template('search.html')

@calendar.route('/timer.html')
def pomo():
    return render_template('timer.html')

@calendar.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@calendar.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@calendar.route('/Day.html')
def Day():
    return render_template('Day.html')

@calendar.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@calendar.route('/Event.html')
def Event():
    return render_template('Event.html')

@calendar.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@calendar.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@calendar.route('/Group.html')
def Group():
    return render_template('Group.html')

@calendar.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@calendar.route('/Invite.html')
def invite():
    return render_template('Invite.html')

@calendar.route('/calendar', methods=['POST'])
def calendar1():
    data = request.get_json()
    tanggal = data.get('tanggal')
    try:
        if len(tanggal) > 0:
            for id_tgl, tgl in tanggal.items():
                calendar_table = ccalendar.query.get(id_tgl)
                calendar_table.date = tgl
                db.session.commit()
            return jsonify({'success': True, 'save': False})
        else:
            calendar_table = ccalendar(
                name=data.get('name'),
                colour=data.get('colour')
            )
            db.session.add(calendar_table)
            db.session.commit()
            return jsonify({'success': True , 'message': 'Task added successfully', 'save': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e), 'save': False})

@calendar.route('/getcalendar', methods=['GET'])
def getcalendar():
    tasks_ = ccalendar.query.all()
    res = []
    for task in tasks_:
        res.append(
            {
                'id': task.id,
                'name': task.name,
                'colour': task.colour,
                'date': task.date
            }
        )
    return jsonify({'status': 'success', 'tasks': res}), 200

@calendar.route('/delete-session/<int:id>', methods=['GET'])
def delete_session(id):
    try:
        session = ccalendar.query.get(id)
        db.session.delete(session)
        db.session.commit()
        return jsonify({'success': True, "message": "Session deleted successfully"})
    except Exception as e:
        return jsonify({'success':False, 'message': str(e)}), 400

if __name__ == '__main__':
    calendar.run(debug=True)