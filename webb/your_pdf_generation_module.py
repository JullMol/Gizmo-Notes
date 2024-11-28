from fpdf import FPDF

def generate_pdf(note_content):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, note_content)

    pdf_file_path = 'note.pdf'
    pdf.output(pdf_file_path)

    return pdf_file_path