import sqlite3
import os

def get_db():
    db_path = os.path.join(os.path.dirname(__file__), '..', 'attendance.db')
    return sqlite3.connect(db_path)
