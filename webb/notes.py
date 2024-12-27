from flask import  Flask , render_template, request, redirect, url_for, Blueprint, jsonify
from .database import db, notes_data
from datetime import datetime
from flask_login import login_required, current_user

notes = Blueprint("notes", __name__)

project_list = []

@notes.route('/save_note', methods=['POST'])
@login_required
def save_note():
    data = request.get_json()
    day = data.get('day')
    note = data.get('content')
    photolist = data.get('photolist')
    try:
        note = notes_data(user_id=current_user.id, hari=day, content=note, photo=photolist)
        db.session.add(note)
        db.session.commit()
        return jsonify({'message': 'Note saved', 'success': True})
    except Exception as e:
        return jsonify({'message': str(e), 'success': False})

@notes.route('/get_notes', methods=['GET'])
@login_required
def get_notes():
    notes = notes_data.query.filter_by(user_id=current_user.id).all()
    return jsonify([{ 
                        'id': note.id,
                        'day': note.hari,
                     'content': note.content,
                      'photolist': note.photo
                    }
                       for note in notes])

@notes.route('/delete_note/<int:note_id>', methods=['GET'])
@login_required
def delete_notes(note_id):
    try:
        note = notes_data.query.get(note_id)
        db.session.delete(note)
        db.session.commit()
        return jsonify({'message': 'Note deleted', 'success': True})
    except Exception as e:
        return jsonify({'message': str(e), 'success': False})

if __name__ == '__main__':
    notes.run(debug=True)