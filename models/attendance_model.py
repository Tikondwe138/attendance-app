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
