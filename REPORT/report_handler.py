from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
import os
from DB import firebase_handler as fh

def split_to_five_words(text):
    words = text.split()
    return '\n'.join([' '.join(words[i:i+5]) for i in range(0, len(words), 5)])

def calculate_column_width(text, base_width=50):
    return base_width * len(split_to_five_words(text).split("\n"))

def severity_to_color(severity):
    color_scale = [
        colors.HexColor("#900C3F"),
        colors.HexColor("#C70039"),
        colors.HexColor("#F94C10"),
        colors.HexColor("#F8DE22"),
        colors.HexColor("#EBE76C"),
        colors.HexColor("#F7E987"),
        colors.HexColor("#FFEECC"),
        colors.HexColor("#FFF6E0"),
        colors.HexColor("#EEEEEE"),
        colors.HexColor("#EEEDED")
    ]

    return color_scale[min(max(0, severity - 1), len(color_scale) - 1)]

def generate_report(filename="DoctorReport.pdf"):
    filename = os.path.join("reports", filename)
    directory = os.path.dirname(filename)
    if directory and not os.path.exists(directory):
        os.makedirs(directory)

    #todo #when run manualy uncomment this to connect to DB
    #fh.initialize_db()
    records = fh.users_sorted_by_severity()

    max_width = max([calculate_column_width(r['conversation_txt']) for r in records])

    data = [["Date", "Name", "Phone", "Symptoms", "Conversation Summary", "Severity"]]
    data += [
        [r['date'], r['name'], r['phone'], r['symptom'], split_to_five_words(r['conversation_txt']), r['severity']] for r in records
    ]

    doc = SimpleDocTemplate(filename, pagesize=landscape(letter))
    table = Table(data, colWidths=[80, 80, 80, 130, max_width, 60])
    table.setStyle(create_style(records))
    doc.build([table])

    print(f"PDF saved as {os.path.abspath(filename)}")

def create_style(records):
    header_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#749BC2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 7.5),
        ('TOPPADDING', (0, 0), (-1, 0), 2.5),
        ('LEFTPADDING', (0, 0), (-1, 0), 40),
        ('RIGHTPADDING', (0, 0), (-1, 0), 40),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#F1F0E8")),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]
    severity_styles = [('BACKGROUND', (-1, i), (-1, i), severity_to_color(r['severity'])) for i, r in enumerate(records, 1)]

    return TableStyle(header_style + severity_styles)
