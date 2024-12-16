from flask_sqlalchemy import SQLAlchemy
from datetime import time
from marshmallow import Schema, fields

# Inisialisasi SQLAlchemy
db = SQLAlchemy()

# Model Database
class Timer(db.Model):
    __tablename__ = 'timers'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    task = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime, nullable=False)

class TimerSchema(Schema):
    id = fields.Integer(dump_only=True)
    start_time = fields.DateTime()
    end_time = fields.DateTime()
    task = fields.String(required=True)
    status = fields.String(required=True)
    duration = fields.Integer(required=True)
    date = fields.DateTime(dump_only=True)

   
class GGoals(db.Model):
    __tablename__ = 'goals'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    your_goals = db.Column(db.String, nullable=False)
    session = db.Column(db.String, nullable=False)
    time_to_achieve_goals = db.Column(db.Date, nullable=False)
    

class GGoalsSchema(Schema):
    id = fields.Integer(dump_only=True)
    your_goals = fields.String()
    session = fields.String()
    time_to_achieve_goals = fields.DateTime()

class pproject(db.Model):
    __tablename__ = 'project'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    project_name = db.Column(db.String, nullable=False)
    session2 = db.Column(db.String, nullable=False)
    time_created = db.Column(db.DateTime, nullable=False)
    time_finished = db.Column(db.DateTime, nullable=False)

class pprojectSchema(Schema):
    id = fields.Integer(dump_only=True)
    project_name = fields.String()
    session2 = fields.String()
    time_created = fields.DateTime()
    time_finished = fields.DateTime()

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
    placement = db.Column(db.String(50), nullable=False)
    activities = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)

class ToDoListE(db.Model):
    __tablename__ = 'todo_listsE'
    
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    placement = db.Column(db.String(50), nullable=False)
    activities = db.Column(db.String(50), nullable=False)
    priority = db.Column(db.String(50), nullable=False)

class Member(db.Model):
    __tablename__ = 'members'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())