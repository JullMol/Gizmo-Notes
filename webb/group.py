from flask import Flask, render_template, Blueprint, jsonify, request
import requests
from dotenv import load_dotenv
import os

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
def invite():
    return render_template('Invite.html')

@group.route('/members', methods=['GET'])
def get_members_from_invite():
    try:
        # Mengambil data anggota dari API invite.py
        response = requests.get('http://localhost:5000/api/members')  # Gantilah URL jika perlu
        if response.status_code == 200:
            members = response.json()  # Data anggota yang diterima dalam bentuk JSON
            
            # Cetak data anggota ke terminal
            print("Data Anggota:", members)  # Menampilkan data anggota di terminal

            # Kembalikan data anggota sebagai JSON (optional, jika ingin mengirim ke frontend)
            return jsonify(members)
        else:
            print("Gagal mengambil data anggota. Status:", response.status_code)
            return jsonify({"error": "Failed to fetch members"}), 500
    except requests.exceptions.RequestException as e:
        print("Error saat melakukan request:", str(e))
        return jsonify({"error": str(e)}), 500
    
@group.route('/api/add_schedule', methods=['POST'])
def add_schedule():
    try:
        # Ambil data schedule dari request
        schedule_data = request.json
        
        # Tambahkan schedule ke list
        schedules.append(schedule_data)
        
        # Kembalikan respons sukses
        return jsonify({"message": "Schedule added successfully", "schedules": schedules}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@group.route('/api/get_schedules', methods=['GET'])
def get_schedules():
    return jsonify(schedules)

@group.route('/api/bot_invite', methods=['GET'])
def bot_invite():
    invite_link = "https://discord.gg/CC8Q36Su"
    return jsonify({"invite_link": invite_link}), 200

if __name__ == '__main__':
    group.run(debug=True, port=5002)