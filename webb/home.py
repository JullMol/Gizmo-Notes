from flask import Flask, render_template, Blueprint
from flask_login import login_required

home = Blueprint('home', __name__)

@home.route('/search.html')
@login_required
def search():
    return render_template('search.html')

@home.route('/timer.html')
@login_required
def pomo():
    return render_template('timer.html')

@home.route('/notesD.html')
@login_required
def notesD():
    return render_template('notesD.html')

@home.route('/notesG.html')
@login_required
def notesG():
    return render_template('notesG.html')

@home.route('/Day.html')
@login_required
def Day():
    return render_template('Day.html')

@home.route('/Assignment.html')
@login_required
def Assignment():
    return render_template('Assignment.html')

@home.route('/Event.html')
@login_required
def Event():
    return render_template('Event.html')

@home.route('/Reports.html')
@login_required
def Reports():
    return render_template('Reports.html')

@home.route('/Goals.html')
@login_required
def Goals():
    return render_template('Goals.html')

@home.route('/Group.html')
@login_required
def Group():
    return render_template('Group.html')

@home.route('/Calendar.html')
@login_required
def Calendar():
    return render_template('Calendar.html')

@home.route('/Project.html')
@login_required
def Project():
    return render_template('Project.html')

@home.route('/Invite.html')
@login_required
def invite():
    return render_template('Invite.html')

if __name__ == '__main__':
    home.run(debug=True)