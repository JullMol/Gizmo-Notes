from flask_sqlalchemy import SQLAlchemy 
from datetime import time
from flask_login import UserMixin

# Inisialisasi SQLAlchemy
db = SQLAlchemy()

# class User(db.Model, UserMixin):
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(255), unique=True, nullable=False)
#     email = db.Column(db.String(255), unique=True, nullable=False)
#     password = db.Column(db.String(255), nullable=False)
#     email_notif = db.Column(db.JSON, nullable=True, default={})
    
#     timers = db.relationship('Timer', backref='user', lazy=True,
#                            foreign_keys='Timer.user_id')

# Model Database
class Timer(db.Model):
    __tablename__ = 'timers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    task = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)

class GGoals(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    your_goals = db.Column(db.String, nullable=False)
    session = db.Column(db.String, nullable=False)
    time_to_achieve_goals = db.Column(db.Date, nullable=False)

class pproject(db.Model):
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String, nullable=False)
    session2 = db.Column(db.String, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)
    time_finished = db.Column(db.DateTime, nullable=False)

class ccalendar(db.Model):
    __tablename__ = 'calendar'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name =  db.Column(db.String, nullable=False)
    colour = db.Column(db.String, nullable=False)
    date = db.Column(db.JSON)

class notes_data(db.Model):
    __tablename__ = 'notesD'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    hari =  db.Column(db.String, nullable=False)
    content = db.Column(db.Text)
    photo = db.Column(db.JSON)
    
class ToDoListD(db.Model):
    __tablename__ = 'todo_listsD'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    placement = db.Column(db.String(50), nullable=False)
    activities = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)

class ToDoListA(db.Model):
    __tablename__ = 'todo_listsA'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)

class ToDoListE(db.Model):
    __tablename__ = 'todo_listsE'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    location = db.Column(db.String(50), nullable=False)
    details = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.Date, server_default=db.func.current_date())
    
class Schedule(db.Model):
    __tablename__ = 'schedule'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    link = db.Column(db.String, unique=True, nullable=False)
    
class Record(db.Model):
    __tablename__ = 'record'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    channel_type = db.Column(db.String(50), nullable=False)
    channel_name = db.Column(db.String(100), nullable=False)
    link = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())