import sqlite3
import os

def get_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'attendance.db')
    conn = sqlite3.connect(db_path)
    # Enable foreign keys right after connection
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
