
from flask import Flask, render_template, request, redirect, send_file
import sqlite3
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('database/students.db')
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            phone TEXT,
            course TEXT,
            monthly_fee INTEGER,
            deposit INTEGER,
            admission_fee INTEGER,
            admission_date TEXT,
            admission_type TEXT
        )
    """)
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('database/students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students")
    students = c.fetchall()
    conn.close()
    return render_template("index.html", students=students)

@app.route('/admission', methods=['GET', 'POST'])
def admission():
    if request.method == 'POST':
        data = (
            request.form['name'],
            request.form['phone'],
            request.form['course'],
            request.form['monthly_fee'],
            request.form['deposit'],
            request.form['admission_fee'],
            request.form['admission_date'],
            request.form['admission_type']
        )
        conn = sqlite3.connect('database/students.db')
        c = conn.cursor()
        c.execute("""
            INSERT INTO students (name, phone, course, monthly_fee, deposit, admission_fee, admission_date, admission_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        conn.commit()
        student_id = c.lastrowid
        conn.close()
        return redirect(f'/receipt/{student_id}')
    return render_template('admission.html')

@app.route('/receipt/<int:student_id>')
def receipt(student_id):
    conn = sqlite3.connect('database/students.db')
    c = conn.cursor()
    c.execute("SELECT * FROM students WHERE id=?", (student_id,))
    student = c.fetchone()
    conn.close()

    filename = f"receipts/receipt_{student_id}.pdf"
    c = canvas.Canvas(filename)
    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(300, 800, "दळवी अभ्यासिका")
    c.setFont("Helvetica", 10)
    c.drawCentredString(300, 780, "आर एम १२४/१, जयभवानी चौक, बजाजनगर, एम.आय.डी.सी.")
    c.drawCentredString(300, 768, "चापूर, संभाजीनगर | Cell: 9404040730, 8459802828")

    y = 740
    c.setFont("Helvetica", 12)
    c.drawString(50, y, f"पावती क्र: DA{student[0]}")
    c.drawRightString(550, y, "दिनांक: __ / __ / ____")
    y -= 30

    c.drawString(50, y, f"नाव: {student[1]}")
    y -= 30

    c.drawString(50, y, "अ.क्र.")
    c.drawString(100, y, "तपशील")
    c.drawString(300, y, "रुपये")
    y -= 20

    details = [
        ("1", "मासिक शुल्क", student[4]),
        ("2", "अनामत रकम", student[5]),
        ("3", "प्रवेश शुल्क", student[6]),
        ("4", "प्रवेश दिनांक", student[7]),
        ("5", "प्रवेश प्रकार", student[8]),
        ("6", f"प्रवेश क्रमांक - DA{student[0]}", "")
    ]

    for num, label, value in details:
        c.drawString(50, y, num)
        c.drawString(100, y, label)
        if value:
            c.drawString(300, y, str(value))
        y -= 20

    c.line(50, y-10, 550, y-10)
    c.drawString(50, y-40, "अक्षरी रू.: ___________________")
    c.drawRightString(550, y-40, "सुपुर्त : __________")
    c.save()

    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    if not os.path.exists("database"):
        os.mkdir("database")
    if not os.path.exists("receipts"):
        os.mkdir("receipts")
    init_db()
    app.run(debug=True)
from flask import Flask, render_template

app = Flask(_name_)

@app.route('/')
def home():
    return render_template("index.html")

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    init_db()
    app.run(host='0.0.0.0', port=port)

