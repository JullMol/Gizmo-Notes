from flask import Flask, render_template, Blueprint

home = Blueprint('home', __name__)

@home.route('/')
def index():
    return render_template('home.html')

@home.route('/home.html')
def menu():
    return render_template('home.html')

@home.route('/search.html')
def search():
    return render_template('search.html')

@home.route('/timer.html')
def pomo():
    return render_template('timer.html')

@home.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@home.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@home.route('/Day.html')
def Day():
    return render_template('Day.html')

@home.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@home.route('/Event.html')
def Event():
    return render_template('Event.html')

@home.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@home.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@home.route('/Group.html')
def Group():
    return render_template('Group.html')

@home.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@home.route('/Invite.html')
def invite():
    return render_template('Invite.html')

if __name__ == '__main__':
    home.run(debug=True)