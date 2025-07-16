# services/attendance_service.py

from datetime import date, time
from sqlalchemy.exc import IntegrityError

from constants.attendance_status import AttendanceStatus
from models.attendance_model import Attendance, db


def is_valid_status(status: str) -> bool:
    return AttendanceStatus.is_valid(status)


def has_existing_record(student_id: str, subject: str, date_obj: date) -> bool:
    return db.session.query(Attendance).filter_by(
        student_id=student_id,
        subject=subject,
        date=date_obj
    ).first() is not None


def mark_attendance(student_id: str, subject: str, date_obj: date, time_obj: time, status: str) -> dict:
    """
    Records attendance for a single student. Validates input for format, duplicates, and allowed statuses.
    """
    if not all([student_id, subject, date_obj, time_obj, status]):
        raise ValueError("All attendance fields are required.")

    if not isinstance(date_obj, date) or not isinstance(time_obj, time):
        raise TypeError("Invalid type: date_obj must be a date and time_obj must be a time.")

    if not is_valid_status(status):
        raise ValueError(f"Invalid status: '{status}'. Allowed: {', '.join(AttendanceStatus.list())}")

    if has_existing_record(student_id, subject, date_obj):
        raise ValueError(f"Attendance already exists for {student_id} in {subject} on {date_obj}.")

    attendance = Attendance(
        student_id=student_id.strip(),
        subject=subject.strip(),
        date=date_obj,
        time=time_obj,
        status=status.lower()
    )

    try:
        db.session.add(attendance)
        db.session.commit()
        return {"success": True, "message": "Attendance recorded successfully."}
    except IntegrityError:
        db.session.rollback()
        raise Exception("Database integrity error while saving attendance.")
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Unexpected error: {str(e)}")


def mark_class_attendance(student_ids: list, subject: str, date_obj: date, time_obj: time, status: str) -> dict:
    """
    Records attendance for multiple students. Skips duplicates and returns summary.
    """
    if not all([student_ids, subject, date_obj, time_obj, status]):
        raise ValueError("All fields are required.")

    if not isinstance(student_ids, list):
        raise TypeError("student_ids must be a list.")

    if not is_valid_status(status):
        raise ValueError(f"Invalid status: '{status}'. Allowed: {', '.join(AttendanceStatus.list())}")

    saved = 0
    skipped = []

    for sid in student_ids:
        sid_clean = sid.strip()
        if has_existing_record(sid_clean, subject, date_obj):
            skipped.append(sid_clean)
            continue

        record = Attendance(
            student_id=sid_clean,
            subject=subject.strip(),
            date=date_obj,
            time=time_obj,
            status=status.lower()
        )
        db.session.add(record)
        saved += 1

    try:
        db.session.commit()
        return {
            "success": True,
            "saved": saved,
            "skipped": skipped,
            "message": f"{saved} records saved, {len(skipped)} skipped (duplicates)."
        }
    except Exception as e:
        db.session.rollback()
        raise Exception(f"Failed to record class attendance: {str(e)}")
