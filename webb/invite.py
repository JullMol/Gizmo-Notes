from flask import Flask, render_template, Blueprint, request, jsonify
from .database import db, Member
invite = Blueprint('invite', __name__)

members = {}

@invite.route('/')
def index():
    return render_template('home.html')

@invite.route('/invite.html')
def menu():
    return render_template('home.html')

@invite.route('/search.html')
def search():
    return render_template('search.html')

@invite.route('/timer.html')
def pomo():
    return render_template('timer.html')

@invite.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@invite.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@invite.route('/Day.html')
def Day():
    return render_template('Day.html')

@invite.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@invite.route('/Event.html')
def Event():
    return render_template('Event.html')

@invite.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@invite.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@invite.route('/Group.html')
def Group():
    return render_template('Group.html')

@invite.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@invite.route('/Invite.html')
def discord():
    
    return render_template('Invite.html')

@invite.route('/api/members/<name_member>', methods=['GET'])
@invite.route('/api/members/', methods=['GET'])
def get_members(name_member=None):
    all_member = Member.query.all()
    members_data = {}
    for member in all_member:
        print(member.name)
        members_data[member.name] = {
        'name': member.name,
        'email': member.email,
        'phone': member.phone,
        'role': member.role
        }
    if name_member is not None:
        member = Member.query.filter_by(name=name_member).first()
        if member:
            db.session.delete(member)
            db.session.commit()
    return jsonify(members_data)

@invite.route('/invite', methods=['POST'])
def invite_member():
    data = request.get_json()
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')
    
    if not all([name, email, phone, role]):
        return jsonify({'message': 'All fields are required'}), 400
    
    new_member = Member(name=name, email=email, phone=phone, role=role)
    try:
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Member invited successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error adding member', 'error': str(e)})
    
if __name__ == '__main__':
    invite.run(debug=True)