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

@group.route('/members', methods=['POST'])
def get_members():
    return jsonify(members)  # Mengembalikan data anggota yang ada di memori

@group.route('/api/hello', methods=['GET'])
def api_hello():
    return jsonify({"message": "Hello from Flask!"})

@group.route('/invite-bot', methods=['GET'])
def invite_bot():
    url = f"{DISCORD_API_BASE_URL}/channels/{CHANNEL_ID}/invites"
    headers = {
        "Authorization": f"Bot {DISCORD_BOT_TOKEN}",
        "Content-Type": "grouplication/json"
    }
    payload = {
        "max_age": 3600,  # Link valid selama 1 jam
        "max_uses": 1,    # Maksimum 1 pengguna
        "temporary": False,
        "unique": True
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        invite = response.json()
        return jsonify({"invite_link": f"https://discord.gg/{invite['code']}"})
    else:
        return jsonify({"error": "Failed to generate invite"}), 500

if __name__ == '__main__':
    group.run(debug=True, port=5002)