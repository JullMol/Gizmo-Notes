import os
from flask import Flask
from flask_mail import Mail, Message
from jinja2 import Template
from datetime import datetime
from .database import Users
from . import mail

def daily_reminder():
    template_path = 'webb/templates/reminder.html'
    try:
        with open(template_path, 'r', encoding='utf-8') as file:
            template = Template(file.read())
    except FileNotFoundError:
        print("Template file not found!")
        return

    users = Users.query.all()
    if not users:
        print("No users found!")
        return

    for user in users:
        todoD = user.todo_listsD
        todoA = user.todo_listsA
        todoE = user.todo_listsE

        rendered_html = template.render(
            user=user.username,
            todoD=todoD,
            todoA=todoA,
            todoE=todoE
        )

        msg = Message(
            subject="To-Do List Reminder",
            recipients=[user.email],
            html=rendered_html
        )

        try:
            mail.send(msg)
            print(f"Email sent to {user.email}")
        except Exception as e:
            print(f"Failed to send email to {user.email}: {e}")