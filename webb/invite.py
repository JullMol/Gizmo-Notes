from flask import Flask, render_template, Blueprint, request, jsonify
from .database import db, Member
invite = Blueprint('invite', __name__)
from flask_login import login_required, current_user

members = {}

@invite.route('/api/members/<name_member>', methods=['GET'])
@invite.route('/api/members/', methods=['GET'])
@login_required
def get_members(name_member=None):
    all_member = Member.query.filter_by(user_id=current_user.id).all()
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
@login_required
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
    
    new_member = Member(user_id=current_user.id, name=name, email=email, phone=phone, role=role)
    try:
        db.session.add(new_member)
        db.session.commit()
        return jsonify({'message': 'Member invited successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error adding member', 'error': str(e)})
    
if __name__ == '__main__':
    invite.run(debug=True)