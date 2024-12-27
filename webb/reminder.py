import os
from flask import session
from flask_mail import Message
from jinja2 import Template
# from website.models import User
from webb import templates
from datetime import datetime, timezone

def daily_reminder():
    # Membaca template HTML dari file reminder.html
    template_path = os.path.join(os.getcwd(), 'webb/templates/reminder.html')  # Sesuaikan path jika perlu
    with open(template_path, 'r', encoding='utf-8') as file:
        template = Template(file.read())

    # Mendapatkan daftar pengguna yang mengaktifkan notifikasi harian
    # users = User.query.filter(User.email_notif['daily_reminder']).all()

    # Mengirim email ke setiap pengguna
    # for user in users:
    #     msg = Message(
    #         subject="Pengingat Harian",
    #         recipients=[user.email],
    #         html=template.render(user=user.username)  # Render template dengan data pengguna
    #     )
    #     templates.send(msg)
