from flask import Flask, render_template, Blueprint, jsonify, request
from .database import db, Schedule
from datetime import datetime
import requests
from dotenv import load_dotenv
import os
import uuid

load_dotenv(".env")
DISCORD_BOT_TOKEN = os.getenv("DISCORD_BOT_TOKEN") 
DISCORD_API_BASE_URL = os.getenv("DISCORD_API_BASE_URL")
CHANNEL_ID = os.getenv("CHANNEL_ID")

group = Blueprint('group', __name__)

members = []
schedules = []

@group.route('/')
def index():
    return render_template('home.html')

@group.route('/home.html')
def menu():
    return render_template('home.html')

@group.route('/search.html')
def search():
    return render_template('search.html')

@group.route('/timer.html')
def pomo():
    return render_template('timer.html')

@group.route('/notesD.html')
def notesD():
    return render_template('notesD.html')

@group.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@group.route('/Day.html')
def Day():
    return render_template('Day.html')

@group.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@group.route('/Event.html')
def Event():
    return render_template('Event.html')

@group.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@group.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@group.route('/Group.html')
def Gizmo():
    return render_template('Group.html')

@group.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@group.route('/Invite.html')
def Vite():
    return render_template('Invite.html')

@group.route('/invite')
def invi():
    return render_template('Invite.html')

@group.route('/members', methods=['GET', 'POST'])
def manage_members():
    global members
    if request.method == 'GET':
        # Logika untuk mendapatkan data anggota dari sumber eksternal
        try:
            response = requests.get('http://localhost:5000/api/members')  # URL API eksternal
            if response.status_code == 200:
                external_members = response.json()
                # Gabungkan dengan anggota lokal jika diperlukan
                all_members = members + external_members
                print("Data Anggota:", all_members)
                return jsonify(all_members)
            else:
                print("Gagal mengambil data anggota eksternal. Status:", response.status_code)
                return jsonify({"error": "Failed to fetch external members"}), 500
        except requests.exceptions.RequestException as e:
            print("Error saat melakukan request:", str(e))
            return jsonify({"error": str(e)}), 500

    elif request.method == 'POST':
        # Logika untuk menyimpan data anggota baru
        try:
            new_member = request.json
            members.append(new_member)  # Tambahkan anggota baru ke daftar
            print("Anggota Baru Ditambahkan:", new_member)
            return jsonify({"message": "Member added successfully", "member": new_member}), 201
        except Exception as e:
            print("Error saat menambahkan anggota:", str(e))
            return jsonify({"error": str(e)}), 500
    
@group.route('/api/members/<string:member_id>', methods=['DELETE'])
def delete_member(member_id):
    global members
    try:
        # Cari anggota berdasarkan ID
        members = [member for member in members if member.get('id') != member_id]
        return jsonify({"message": "Member deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@group.route('/api/add_schedule', methods=['POST'])
def add_schedule():
    try:
        # Ambil data schedule dari request
        schedule_data = request.json
        
        if not schedule_data.get('date') or not schedule_data.get('subject') or not schedule_data.get('link'):
            return jsonify({"error": "All fields (date, subject, link) are required!"}), 400
        
        try:
            date_s = datetime.strptime(schedule_data['date'], '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid date format!"}), 400
            
        new_schedule = Schedule(
            date=date_s,
            subject=schedule_data['subject'],
            link=schedule_data['link']
        )
        
        db.session.add(new_schedule)
        db.session.commit()
        
        # Kembalikan respons sukses
        return jsonify({
            "message": "Schedule added successfully",
            "schedule": {
                "id": new_schedule.id,
                "date": new_schedule.date,
                "subject": new_schedule.subject,
                "link": new_schedule.link
            }
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@group.route('/api/get_schedules', methods=['GET'])
def get_schedules():
    try:
        # Query semua jadwal dari database
        all_schedules = Schedule.query.all()

        # Format data untuk dikembalikan
        schedules_list = [
            {
                "id": schedule.id,
                "date": schedule.date,
                "subject": schedule.subject,
                "link": schedule.link
            }
            for schedule in all_schedules
        ]

        return jsonify(schedules_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@group.route('/api/schedules/<string:schedule_id>', methods=['DELETE'])
def delete_schedule(schedule_id):
    global schedules
    try:
        # Cari jadwal berdasarkan ID
        schedule_to_delete = Schedule.query.get(schedule_id)

        if not schedule_to_delete:
            return jsonify({"error": "Schedule not found"}), 404

        # Hapus dari database
        db.session.delete(schedule_to_delete)
        db.session.commit()

        return jsonify({"message": "Schedule deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@group.route('/api/bot_invite', methods=['GET'])
def bot_invite():
    invite_link = "https://discord.gg/aX78aErJzG"
    return jsonify({"invite_link": invite_link}), 200

if __name__ == '__main__':
    group.run(debug=True, port=5002)