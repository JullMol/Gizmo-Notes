from flask import  Flask , render_template, request, redirect, url_for, Blueprint, jsonify
from .database import db, notes_data
from datetime import datetime

notes = Blueprint("notes", __name__)

project_list = []


@notes.route('/')
def index():
    return render_template('home.html')

@notes.route('/home.html')
def menu():
    return render_template('home.html')

@notes.route('/search.html')
def search():
    return render_template('search.html')

@notes.route('/timer.html')
def pomo():
    return render_template('timer.html')

@notes.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@notes.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@notes.route('/save_note', methods=['POST'])
def save_note():
    data = request.get_json()
    day = data.get('day')
    note = data.get('content')
    photolist = data.get('photolist')
    try:
        note = notes_data(hari=day, content=note, photo=photolist)
        db.session.add(note)
        db.session.commit()
        return jsonify({'message': 'Note saved', 'success': True})
    except Exception as e:
        return jsonify({'message': str(e), 'success': False})

@notes.route('/get_notes', methods=['GET'])
def get_notes():
    notes = notes_data.query.all()
    return jsonify([{ 
                        'id': note.id,
                        'day': note.hari,
                     'content': note.content,
                      'photolist': note.photo
                    }
                       for note in notes])

@notes.route('/delete_note/<int:note_id>', methods=['GET'])
def delete_notes(note_id):
    try:
        note = notes_data.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted', 'success': True})
    except Exception as e:
        return jsonify({'message': str(e), 'success': False})

@notes.route('/Day.html')
def Day():
    return render_template('Day.html')

@notes.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@notes.route('/Event.html')
def Event():
    return render_template('Event.html')

@notes.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@notes.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@notes.route('/Group.html')
def Group():
    return render_template('Group.html')

@notes.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@notes.route('/Invite.html')
def invite():
    return render_template('Invite.html')