from flask import Flask, render_template, request, redirect, send_file
import sqlite3
import os
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

app = Flask(__name__)
DB_PATH = "database/students.db"
RECEIPT_FOLDER = "receipts"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            mobile TEXT,
            address TEXT,
            admission_date TEXT,
            course TEXT,
            fees REAL
        )
    ''')
    conn.commit()
    conn.close()

def generate_receipt(student):
    if not os.path.exists(RECEIPT_FOLDER):
        os.makedirs(RECEIPT_FOLDER)

    filename = os.path.join(RECEIPT_FOLDER, f"receipt_{student['id']}.pdf")
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica", 12)

    c.drawString(100, 750, "Dalvi Abhyasika - Admission Receipt")
    c.drawString(100, 730, f"Date: {datetime.now().strftime('%Y-%m-%d')}")
    c.drawString(100, 700, f"Student ID: {student['id']}")
    c.drawString(100, 680, f"Name: {student['name']}")
    c.drawString(100, 660, f"Mobile: {student['mobile']}")
    c.drawString(100, 640, f"Address: {student['address']}")
    c.drawString(100, 620, f"Course: {student['course']}")
    c.drawString(100, 600, f"Fees: ₹{student['fees']}")

    c.save()
    return filename

@app.route('/')
def home():
    return render_template('admission.html')

@app.route('/submit', methods=['POST'])
def submit():
    name = request.form['name']
    mobile = request.form['mobile']
    address = request.form['address']
    admission_date = request.form['admission_date']
    course = request.form['course']
    fees = float(request.form['fees'])

    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO students (name, mobile, address, admission_date, course, fees) VALUES (?, ?, ?, ?, ?, ?)',
              (name, mobile, address, admission_date, course, fees))
    conn.commit()
    student_id = c.lastrowid
    conn.close()

    student = {
        "id": student_id,
        "name": name,
        "mobile": mobile,
        "address": address,
        "admission_date": admission_date,
        "course": course,
        "fees": fees
    }

    receipt_path = generate_receipt(student)
    return send_file(receipt_path, as_attachment=True)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
