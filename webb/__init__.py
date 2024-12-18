from flask import Flask
from .database import db
import os

app = Flask(__name__)
DB_name = 'local_database_4.db'
def create_app():
    # Konfigurasi database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_name}'  # Menggunakan SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Inisialisasi SQLAlchemy
    db.init_app(app)
    
    from .home import home
    from .timer import timer
    from .group import group
    from .todo import todo
    from .invite import invite
    from .goals import goals
    from .project import project
    from .calendar import calendar
    from .notes import notes
    app.register_blueprint(home)
    app.register_blueprint(timer)
    app.register_blueprint(group)
    app.register_blueprint(todo)
    app.register_blueprint(invite)
    app.register_blueprint(goals)
    app.register_blueprint(project)
    app.register_blueprint(calendar)
    app.register_blueprint(notes)
    
    create_base(app)
    return app

def create_base(app):
    # Membuat tabel jika belum ada
    if not os.path.exists('webb/{DB_name}'):
        with app.app_context():
            db.create_all()  # Membuat semua tabel, termasuk tabel 'members'