from flask import Flask, render_template, Blueprint, request, jsonify, send_from_directory
from fpdf import FPDF

notesD = Blueprint('notesD', __name__)

@notesD.route('/')
def index():
    return render_template('home.html')

@notesD.route('/home.html')
def menu():
    return render_template('home.html')

@notesD.route('/search.html')
def search():
    return render_template('search.html')

@notesD.route('/timer.html')
def pomo():
    return render_template('timer.html')

@notesD.route('/notesD.html')
def noteD():
    return render_template('notesD.html')

@notesD.route('/notesG.html')
def notesG():
    return render_template('notesG.html')

@notesD.route('/Day.html')
def Day():
    return render_template('Day.html')

@notesD.route('/Assignment.html')
def Assignment():
    return render_template('Assignment.html')

@notesD.route('/Event.html')
def Event():
    return render_template('Event.html')

@notesD.route('/Reports.html')
def Reports():
    return render_template('Reports.html')

@notesD.route('/Goals.html')
def Goals():
    return render_template('Goals.html')

@notesD.route('/Group.html')
def Group():
    return render_template('Group.html')

@notesD.route('/Calendar.html')
def Calendar():
    return render_template('Calendar.html')

@notesD.route('/Invite.html')
def invite():
    return render_template('Invite.html')

@notesD.route('/save_note', methods=['POST'])
def save_note():
    data = request.get_json()
    note_content = data.get('note')

    # Simpan catatan ke file
    with open('note.txt', 'w') as f:
        f.write(note_content)

    # Generate PDF dari catatan
    pdf_file_path = generate_pdf(note_content)  # Panggil fungsi generate_pdf

    return jsonify(success=True, pdf_path=pdf_file_path)

def generate_pdf(note_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, note_content)

    pdf_file_path = 'note.pdf'  # Nama file PDF
    pdf.output(pdf_file_path)

    return pdf_file_path

@notesD.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(directory='.', path=filename, as_attachment=True)

if __name__ == '__main__':
    notesD.run(debug=True)