import sqlite3
from database.db_config import get_db

def enable_foreign_keys(conn):
    # SQLite disables FK by default, enable it per connection
    conn.execute("PRAGMA foreign_keys = ON")

def init_db():
    conn = get_db()
    enable_foreign_keys(conn)
    c = conn.cursor()
    
    # Users table - students
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            student_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            student_class TEXT NOT NULL  -- renamed from class to student_class
        )
    ''')

    # Attendance table
    c.execute('''
        CREATE TABLE IF NOT EXISTS attendance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            student_id TEXT NOT NULL,
            subject TEXT NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            status TEXT NOT NULL CHECK(status IN ('present', 'absent', 'late')),
            FOREIGN KEY(student_id) REFERENCES users(student_id)
        )
    ''')

    conn.commit()
    conn.close()

def get_class_students(class_name):
    conn = get_db()
    enable_foreign_keys(conn)
    c = conn.cursor()
    c.execute("SELECT student_id, name FROM users WHERE student_class = ?", (class_name,))
    students = c.fetchall()
    conn.close()
    return [{'student_id': s[0], 'name': s[1]} for s in students]



def add_user(student_id, name, email, password, student_class):
    conn = get_db()
    enable_foreign_keys(conn)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO users (student_id, name, email, password, student_class)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, name, email, password, student_class))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError adding user {student_id}: {e}")
    finally:
        conn.close()

def seed_test_users():
    test_users = [
        ("STU001", "Alice Johnson", "alice.johnson@example.com", "pass123", "Class A"),
        ("STU002", "Bob Smith", "bob.smith@example.com", "pass123", "Class A"),
        ("STU003", "Charlie Brown", "charlie.brown@example.com", "pass123", "Class B"),
        ("STU004", "Diana Prince", "diana.prince@example.com", "pass123", "Class B"),
        # ... add class info for all others similarly
    ]
    for sid, name, email, pwd, cls in test_users:
        add_user(sid, name, email, pwd, cls)

def mark_attendance(student_id, subject, date, time, status):
    conn = get_db()
    enable_foreign_keys(conn)
    c = conn.cursor()
    try:
        c.execute('''
            INSERT INTO attendance (student_id, subject, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        ''', (student_id, subject, date, time, status))
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError marking attendance for {student_id}: {e}")
    finally:
        conn.close()

def mark_attendance_for_class(class_name, subject, date, time, status_map):
    """
    Bulk mark attendance for all students in a class.
    status_map: dict {student_id: status}, e.g. {"STU001": "present", "STU002": "late"}
    """
    conn = get_db()
    enable_foreign_keys(conn)
    c = conn.cursor()
    try:
        # Get all students in class
        c.execute("SELECT student_id FROM users WHERE student_class = ?", (class_name,))
        students = c.fetchall()
        attendance_records = []
        for (student_id,) in students:
            st = status_map.get(student_id, 'absent')  # default absent if not specified
            attendance_records.append((student_id, subject, date, time, st))
        
        c.executemany('''
            INSERT INTO attendance (student_id, subject, date, time, status)
            VALUES (?, ?, ?, ?, ?)
        ''', attendance_records)
        conn.commit()
    except sqlite3.IntegrityError as e:
        print(f"IntegrityError bulk marking attendance for class {class_name}: {e}")
    finally:
        conn.close()

def get_attendance(student_id=None, date=None, subject=None, class_name=None, start_date=None, end_date=None):
    """
    Fetch attendance records filtered by:
    - student_id
    - subject
    - class_name (requires join with users)
    - specific date or date range (start_date, end_date)
    """
    conn = get_db()
    enable_foreign_keys(conn)
    c = conn.cursor()

    base_query = '''
        SELECT a.student_id, u.name, u.student_class, a.subject, a.date, a.time, a.status
        FROM attendance a
        JOIN users u ON a.student_id = u.student_id
        WHERE 1=1
    '''
    params = []

    if student_id:
        base_query += " AND a.student_id = ?"
        params.append(student_id)
    if subject:
        base_query += " AND a.subject = ?"
        params.append(subject)
    if class_name:
        base_query += " AND u.student_class = ?"
        params.append(class_name)
    if date:
        base_query += " AND a.date = ?"
        params.append(date)
    if start_date and end_date:
        base_query += " AND a.date BETWEEN ? AND ?"
        params.append(start_date)
        params.append(end_date)
    elif start_date:
        base_query += " AND a.date >= ?"
        params.append(start_date)
    elif end_date:
        base_query += " AND a.date <= ?"
        params.append(end_date)

    c.execute(base_query, params)
    rows = c.fetchall()
    conn.close()

    return [
        {
            'student_id': row[0],
            'student_name': row[1],
            'student_class': row[2],
            'subject': row[3],
            'date': row[4],
            'time': row[5],
            'status': row[6]
        }
        for row in rows
    ]

def get_attendance_summary(student_id=None, class_name=None, start_date=None, end_date=None):
    """
    Summarize attendance metrics: counts of present, absent, late grouped by student or class.
    """
    conn = get_db()
    enable_foreign_keys(conn)
    c = conn.cursor()

    base_query = '''
        SELECT a.student_id, u.name, u.student_class,
            SUM(CASE WHEN a.status = 'present' THEN 1 ELSE 0 END) AS present_count,
            SUM(CASE WHEN a.status = 'absent' THEN 1 ELSE 0 END) AS absent_count,
            SUM(CASE WHEN a.status = 'late' THEN 1 ELSE 0 END) AS late_count
        FROM attendance a
        JOIN users u ON a.student_id = u.student_id
        WHERE 1=1
    '''
    params = []

    if student_id:
        base_query += " AND a.student_id = ?"
        params.append(student_id)
    if class_name:
        base_query += " AND u.student_class = ?"
        params.append(class_name)
    if start_date and end_date:
        base_query += " AND a.date BETWEEN ? AND ?"
        params.append(start_date)
        params.append(end_date)
    elif start_date:
        base_query += " AND a.date >= ?"
        params.append(start_date)
    elif end_date:
        base_query += " AND a.date <= ?"
        params.append(end_date)

    base_query += " GROUP BY a.student_id"

    c.execute(base_query, params)
    rows = c.fetchall()
    conn.close()

    return [
        {
            'student_id': row[0],
            'student_name': row[1],
            'student_class': row[2],
            'present': row[3],
            'absent': row[4],
            'late': row[5]
        }
        for row in rows
    ]
