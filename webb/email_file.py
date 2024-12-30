from flask import session  # Import session from Flask
from flask_mail import Message
from jinja2 import Template
from . import mail
import os

def send_login_information(email, username, password):
    email_from_session = session.get('email')  # Get email from session
    username_from_session = session.get('username')  # Get username from session
    password_from_session = session.get('password')

    with open(os.path.join(os.getcwd(), 'webb/templates/login_info.html'), 'r', encoding='utf-8') as file:
        template = Template(file.read())
    
    msg = Message(
        "Login Information for gizmonotes",
        recipients=[email],
        html=template.render(username=username, password=password)
    )
    mail.send(msg)