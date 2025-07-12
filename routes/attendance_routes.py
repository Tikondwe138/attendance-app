from flask import Blueprint, render_template, request, jsonify, redirect, url_for, flash, session
from models.attendance_model import Attendance, db
from datetime import datetime

attendance_bp = Blueprint('attendance', __name__)

# --------------------- Individual Attendance ---------------------
@attendance_bp.route('/attendance', methods=['GET', 'POST'])
def attendance():
    if 'user' not in session:
        flash("Please log in first.", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        try:
            student_id = session.get('user')  # assuming students submit their own
            date_str = request.form.get('date')
            time_str = request.form.get('time')
            subject = request.form.get('subject')
            status = request.form.get('status')

            if not all([student_id, date_str, time_str, subject, status]):
                flash("All fields are required.", "error")
                return redirect(url_for('attendance.attendance'))

            date = datetime.strptime(date_str, '%Y-%m-%d').date()
            time = datetime.strptime(time_str, '%H:%M').time()

            record = Attendance(
                student_id=student_id,
                date=date,
                time=time,
                subject=subject,
                status=status
            )
            db.session.add(record)
            db.session.commit()

            flash("Attendance recorded successfully ✅", "success")
            return redirect(url_for('attendance.attendance'))

        except Exception as e:
            flash(f"Error: {str(e)}", "error")
            return redirect(url_for('attendance.attendance'))

    return render_template('attendance.html')


# --------------------- Bulk Attendance ---------------------
@attendance_bp.route('/attendance/bulk', methods=['GET', 'POST'])
def bulk_attendance():
    if 'user' not in session or session.get('role') != 'admin':
        flash("Only admins can mark bulk attendance 😤", "error")
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        return render_template('bulk_attendance.html')

    try:
        data = request.get_json() or request.form
        student_ids = data.get('student_ids')  # expect list from JS
        subject = data.get('subject')
        date_str = data.get('date')
        time_str = data.get('time')
        status = data.get('status')

        if not all([student_ids, subject, date_str, time_str, status]):
            return jsonify({'error': 'Missing required fields'}), 400

        # If it's a string, try to parse it
        if isinstance(student_ids, str):
            student_ids = student_ids.split(',')

        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time = datetime.strptime(time_str, '%H:%M').time()

        for sid in student_ids:
            record = Attendance(
                student_id=sid.strip(),
                date=date,
                time=time,
                subject=subject,
                status=status
            )
            db.session.add(record)

        db.session.commit()
        return jsonify({'message': 'Bulk attendance recorded successfully ✅'})

    except Exception as e:
        return jsonify({'error': f"Something went wrong: {str(e)}"}), 500


# --------------------- Admin Attendance Report (JSON API) ---------------------
@attendance_bp.route('/api/attendance/report', methods=['GET'])
def admin_report_api():
    if 'user' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Access denied'}), 403

    student_id = request.args.get('student_id')
    subject = request.args.get('subject')
    date = request.args.get('date')

    query = Attendance.query

    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    if subject:
        query = query.filter(Attendance.subject == subject)
    if date:
        query = query.filter(Attendance.date == date)

    records = query.order_by(Attendance.date.desc(), Attendance.time.desc()).all()

    result = [
        {
            "student_id": r.student_id,
            "subject": r.subject,
            "date": r.date.strftime('%Y-%m-%d'),
            "time": r.time.strftime('%H:%M'),
            "status": r.status
        } for r in records
    ]

    return jsonify(result)


# --------------------- Export CSV Endpoint ---------------------
@attendance_bp.route('/api/attendance/export/csv', methods=['GET'])
def export_attendance_csv():
    from io import StringIO
    import csv
    from flask import Response

    if 'user' not in session or session.get('role') != 'admin':
        return jsonify({'error': 'Access denied'}), 403

    student_id = request.args.get('student_id')
    subject = request.args.get('subject')
    date = request.args.get('date')

    query = Attendance.query
    if student_id:
        query = query.filter(Attendance.student_id == student_id)
    if subject:
        query = query.filter(Attendance.subject == subject)
    if date:
        query = query.filter(Attendance.date == date)

    records = query.all()

    si = StringIO()
    cw = csv.writer(si)
    cw.writerow(['Student ID', 'Subject', 'Date', 'Time', 'Status'])

    for r in records:
        cw.writerow([
            r.student_id,
            r.subject,
            r.date.strftime('%Y-%m-%d'),
            r.time.strftime('%H:%M'),
            r.status
        ])

    output = si.getvalue()
    return Response(output, mimetype='text/csv', headers={
        "Content-Disposition": "attachment; filename=attendance_report.csv"
    })
