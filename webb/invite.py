from flask import Flask, render_template, Blueprint, request, jsonify

invite = Blueprint('invite', __name__)

members = []

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

@invite.route('/invite', methods=['POST'])
def dc():
    # Menerima data JSON yang dikirim oleh invite.js
    data = request.get_json()

    # Cek apakah semua data diperlukan ada
    if 'name' not in data or 'email' not in data or 'phone' not in data or 'role' not in data:
        return jsonify({'error': 'Missing data'}), 400

    # Simpan data anggota ke dalam list di memori
    member_data = {
        'name': data['name'],
        'email': data['email'],
        'phone': data['phone'],
        'role': data['role']
    }

    members.append(member_data)  # Menambahkan ke list members
    print(members)
    return jsonify({'message': 'Member added successfully!'}), 201
if __name__ == '__main__':
    invite.run(debug=True)