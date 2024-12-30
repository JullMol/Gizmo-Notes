from flask import Flask, render_template, Blueprint, jsonify, request
from .database import db, ccalendar
from datetime import datetime
from flask_login import login_required, current_user
calendar = Blueprint('calendar', __name__)

# calendar = []
@calendar.route('/calendar', methods=['POST'])
@login_required
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
                colour=data.get('colour'),
                user_id=current_user.id
            )
            db.session.add(calendar_table)
            db.session.commit()
            return jsonify({'success': True , 'message': 'Task added successfully', 'save': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e), 'save': False})

@calendar.route('/getcalendar', methods=['GET'])
@login_required
def getcalendar():
    tasks_ = ccalendar.query.filter_by(user_id=current_user.id).all()
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
@login_required
def delete_session(id):
    try:
        session = ccalendar.query.get(id)
        db.session.delete(session)
        db.session.commit()
        return jsonify({'success': True, "message": "Session deleted successfully"})
    except Exception as e:
        return jsonify({'success':False, 'message': str(e)}), 400