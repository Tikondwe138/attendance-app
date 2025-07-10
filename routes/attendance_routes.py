from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from models.attendance_model import Attendance, db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)


# --------------------- Individual Attendance (Users) ---------------------
@attendance_bp.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if request.method == 'POST':
        try:
            date_str = request.form.get('date')
            time_str = request.form.get('time')
            subject = request.form.get('subject')
            status = request.form.get('status')

            if not all([date_str, time_str, subject, status]):
                flash("All fields are required.", "error")
                return redirect(url_for('attendance.attendance'))

            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()

            attendance_record = Attendance(
                date=date,
                time=time,
                subject=subject,
                status=status
            )
            db.session.add(attendance_record)
            db.session.commit()

            flash("Attendance recorded successfully.", "success")
            return redirect(url_for('attendance.attendance'))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('attendance.attendance'))

    return render_template('attendance.html')


# --------------------- Admin Attendance Report ---------------------
@attendance_bp.route('/attendance/report', methods=['GET'])
def attendance_report_admin():
    # Optional: Restrict access
    # if session.get('user') != 'admin':
    #     flash("Access denied. Admins only.", "error")
    #     return redirect(url_for('attendance.attendance'))

    subject = request.args.get('subject')
    status = request.args.get('status')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    query = Attendance.query

    if subject:
        query = query.filter(Attendance.subject == subject)
    if status:
        query = query.filter(Attendance.status == status)
    if date_from:
        query = query.filter(Attendance.date >= date_from)
    if date_to:
        query = query.filter(Attendance.date <= date_to)

    records = query.order_by(Attendance.date.desc(), Attendance.time.desc()).all()
    return render_template('attendance_report_admin.html', records=records)


# --------------------- Bulk Attendance (Admins) ---------------------
@attendance_bp.route('/attendance/bulk', methods=['GET', 'POST'])
def bulk_attendance():
    if request.method == 'GET':
        return render_template('bulk_attendance.html')

    try:
        # Works for both JSON and form submission
        data = request.get_json() or request.form

        student_ids_raw = data.get('student_ids')
        subject = data.get('subject')
        date_str = data.get('date')
        time_str = data.get('time')
        status = data.get('status')

        if not all([student_ids_raw, subject, date_str, time_str, status]):
            flash("Missing required fields.", "error")
            return redirect(url_for('attendance.bulk_attendance'))

        # Split comma-separated input into a list
        student_ids = [s.strip() for s in student_ids_raw.split(',')]

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()

        for student_id in student_ids:
            record = Attendance(
                student_id=student_id,
                date=date,
                time=time,
                subject=subject,
                status=status
            )
            db.session.add(record)

        db.session.commit()
        flash("Bulk attendance recorded successfully.", "success")
        return redirect(url_for('attendance.bulk_attendance'))

    except Exception as e:
        flash(f"Error: {str(e)}", "error")
        return redirect(url_for('attendance.bulk_attendance'))
