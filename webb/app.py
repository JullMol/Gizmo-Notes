from flask import Flask
from database import db, Member  # Import db dan Member dari database.py

app = Flask(__name__)

# Konfigurasi database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///local_database_3.db'  # Menggunakan SQLite
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Inisialisasi SQLAlchemy
db.init_app(app)

# Membuat tabel jika belum ada
with app.app_context():
    db.create_all()  # Membuat semua tabel, termasuk tabel 'members'

@app.route('/')
def home():
    return "Database and tables created!"

if __name__ == '__main__':
    app.run(debug=True)