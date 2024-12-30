from flask import Flask
from .database import db, Users
import os
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from dotenv import load_dotenv

load_dotenv('webb/.env')
login_manager = LoginManager()
login_manager.login_view = 'auth.auth_page'
mail =  Mail()
app = Flask(__name__)
DB_name = 'local_database.db'
migrate = Migrate()
BOT_TOKEN = os.getenv("BOT_TOKEN")
def create_app():
    # Konfigurasi database
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(app.static_folder ,DB_name)}'  # Menggunakan SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 465
    app.config['MAIL_USE_TLS'] = False
    app.config['MAIL_USE_SSL'] = True
    app.config['MAIL_USERNAME'] = os.getenv('GMAIL_EMAIL')
    app.config['MAIL_PASSWORD'] = os.getenv('GMAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv('GMAIL_EMAIL')
    
    # Inisialisasi SQLAlchemy
    db.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    
    from .home import home
    from .timer import timer
    from .group import group
    from .todo import todo
    from .invite import invite
    from .goals import goals
    from .project import project
    from .app_calendar import calendar
    from .notes import notes
    from .auth import auth
    
    app.register_blueprint(home)
    app.register_blueprint(timer)
    app.register_blueprint(group)
    app.register_blueprint(todo)
    app.register_blueprint(invite)
    app.register_blueprint(goals)
    app.register_blueprint(project)
    app.register_blueprint(calendar)
    app.register_blueprint(notes)
    app.register_blueprint(auth)
    
    @login_manager.user_loader
    def load_user(id):
        return Users.query.get(int(id))
    # create_base(app)
    return app

# def create_base(app):
#     # Membuat tabel jika belum ada
#     if not os.path.exists('webb/{DB_name}'):
#         with app.app_context():
#             db.create_all()  # Membuat semua tabel, termasuk tabel 'members'

# @app.route('/api/bot_invite', methods=['GET'])
# def bot_invite():
#     invite_link = os.getenv('personal_bot_link')
#     return {"invite_link": invite_link}, 200

# @app.route('/run_bot', methods=['GET'])
# def run_bot():
#     from .tes import run_bot
#     try:
#         run_bot()
#     except Exception as e:
#         return str(e), 500