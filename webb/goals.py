from flask import Flask, render_template, Blueprint, jsonify, request
from .database import db, GGoals, GGoalsSchema
from datetime import datetime

goals = Blueprint('goals', __name__)

Goals = []

@goals.route('/')
def index():
    return render_template('home.html')

@goals.route('/home.html')
def menu():
    return render_template('home.html')

@goals.route('/search.html')
def search():
    return render_template('search.html')

@goals.route('/timer.html')
def pomo():
    return render_template('timer.html')

@goals.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@goals.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@goals.route('/Day.html')
def Day():
    return render_template('Day.html')

@goals.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@goals.route('/Event.html')
def Event():
    return render_template('Event.html')

@goals.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@goals.route('/Goals.html')
def Goal():
    return render_template('Goals.html')

@goals.route('/Group.html')
def Group():
    return render_template('Group.html')

@goals.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@goals.route('/Invite.html')
def invite():
    return render_template('Invite.html')


@goals.route('/savegoals', methods=['POST'])
def SaveGoals():
    data = request.get_json()
    tm = data.get('timeachieve')
    tm_ = datetime.strptime(tm, '%Y-%m-%dT%H:%M')
    goals_table = GGoals(
        your_goals=data.get('goalss'),
        session=data.get('session'),
        time_to_achieve_goals=tm_,
    )
    db.session.add(goals_table)
    db.session.commit()

    # print(f"Task added for {date}: {task}")
    return jsonify({'status': 'success', 'message': 'Task added successfully'}), 200

if __name__ == '__main__':
    goals.run(debug=True)