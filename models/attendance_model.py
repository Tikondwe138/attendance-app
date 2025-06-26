import sqlite3
from database.db_config import get_db

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

def mark_attendance(student_id, subject, date, time, status):
    conn = get_db()
    c = conn.cursor()
    c.execute('''
        INSERT INTO attendance (student_id, subject, date, time, status)
        VALUES (?, ?, ?, ?, ?)
    ''', (student_id, subject, date, time, status))
    conn.commit()
    conn.close()

def get_attendance(student_id=None, date=None, subject=None):
    conn = get_db()
    c = conn.cursor()
    query = "SELECT student_id, subject, date, time, status FROM attendance WHERE 1=1"
    params = []
    if student_id:
        query += " AND student_id = ?"
        params.append(student_id)
    if date:
        query += " AND date = ?"
        params.append(date)
    if subject:
        query += " AND subject = ?"
        params.append(subject)
    c.execute(query, params)
    rows = c.fetchall()
    conn.close()
    return [
        {
            'student_id': row[0],
            'subject': row[1],
            'date': row[2],
            'time': row[3],
            'status': row[4]
        } for row in rows
    ]
