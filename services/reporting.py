# services/reporting.py

from datetime import date
from sqlalchemy import func

from models.attendance_model import Attendance, db
from constants.attendance_status import AttendanceStatus


def get_student_attendance_summary(student_id: str, start_date: date, end_date: date) -> dict:
    """
    Returns count of present, absent, and tardy entries for a student between two dates.
    """
    summary = {status: 0 for status in AttendanceStatus.list()}

    results = db.session.query(Attendance.status, func.count().label("count")) \
        .filter(
            Attendance.student_id == student_id,
            Attendance.date >= start_date,
            Attendance.date <= end_date
        ) \
        .group_by(Attendance.status).all()

    for status, count in results:
        status_key = status.lower()
        if status_key in summary:
            summary[status_key] = count

    return summary


def get_class_attendance_rate(subject: str, start_date: date, end_date: date) -> dict:
    """
    Returns attendance rate (percentage of present entries) for a given subject and date range.
    """
    total = db.session.query(Attendance).filter(
        Attendance.subject == subject,
        Attendance.date >= start_date,
        Attendance.date <= end_date
    ).count()

    if total == 0:
        return {"attendance_rate": 0.0}

    present = db.session.query(Attendance).filter(
        Attendance.subject == subject,
        Attendance.date >= start_date,
        Attendance.date <= end_date,
        Attendance.status == AttendanceStatus.PRESENT.value
    ).count()

    rate = (present / total) * 100
    return {"attendance_rate": round(rate, 2)}


def get_filtered_attendance_list(
    status_filter: str,
    subject: str = None,
    start_date: date = None,
    end_date: date = None
) -> list:
    """
    Returns filtered attendance records by status (e.g. 'absent', 'tardy').
    Optional filters: subject, date range.
    """
    if not AttendanceStatus.is_valid(status_filter):
        raise ValueError(f"Invalid status: '{status_filter}'. Allowed: {', '.join(AttendanceStatus.list())}")

    query = db.session.query(Attendance).filter(Attendance.status == status_filter.lower())

    if subject:
        query = query.filter(Attendance.subject == subject)
    if start_date:
        query = query.filter(Attendance.date >= start_date)
    if end_date:
        query = query.filter(Attendance.date <= end_date)

    results = query.order_by(Attendance.date.desc(), Attendance.time.desc()).all()

    return [
        {
            "student_id": r.student_id,
            "subject": r.subject,
            "date": r.date.strftime("%Y-%m-%d"),
            "time": r.time.strftime("%H:%M"),
            "status": r.status
        }
        for r in results
    ]
