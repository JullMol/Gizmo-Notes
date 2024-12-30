import os
# os.chdir('./Gizmo-Notes')
from app import app
from webb import reminder
# from webb import create_app

if __name__ == "__main__":
    with app.app_context():
        reminder.daily_reminder()