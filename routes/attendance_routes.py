from flask import Blueprint, render_template, request, jsonify, send_file
from models.attendance_model import init_db, mark_attendance, mark_attendance_for_class, get_attendance, get_class_students
import csv
import io

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance')
def attendance():
    return render_template('attendance.html')

@attendance_bp.route('/api/attendance/mark', methods=['POST'])
def mark():
    data = request.json
    try:
        if data.get('class_id'):
            # Mark attendance for whole class using bulk function
            class_name = data['class_id']  # assuming class_id == class_name (fix if needed)
            status_map = {}  # if you want all same status, build this map
            student_ids = get_class_students(class_name)
            for sid in student_ids:
                status_map[sid] = data['status']
            mark_attendance_for_class(
                class_name,
                data['subject'],
                data['date'],
                data['time'],
                status_map
            )
            return jsonify({"message": f"Attendance marked for class {class_name}"}), 200
        elif data.get('student_id'):
            mark_attendance(
                data['student_id'],
                data['subject'],
                data['date'],
                data['time'],
                data['status']
            )
            return jsonify({"message": "Attendance marked successfully"}), 200
        else:
            return jsonify({"error": "student_id or class_id required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@attendance_bp.route('/api/attendance/report', methods=['GET'])
def attendance_report():
    student_id = request.args.get('student_id')
    class_id = request.args.get('class_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    subject = request.args.get('subject')

    records = []
    try:
        if class_id:
            records = get_attendance(
                class_name=class_id,
                subject=subject,
                start_date=date_from,
                end_date=date_to
            )
        elif student_id:
            records = get_attendance(
                student_id=student_id,
                subject=subject,
                start_date=date_from,
                end_date=date_to
            )
        else:
            return jsonify({"error": "student_id or class_id required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify(records)

@attendance_bp.route('/attendance-report-admin')
def attendance_report_admin():
    return render_template('attendance_report_admin.html')


@attendance_bp.route('/api/attendance/export/csv', methods=['GET'])
def export_attendance_csv():
    student_id = request.args.get('student_id')
    class_id = request.args.get('class_id')
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')
    subject = request.args.get('subject')

    records = []
    try:
        if class_id:
            records = get_attendance(
                class_name=class_id,
                subject=subject,
                start_date=date_from,
                end_date=date_to
            )
        elif student_id:
            records = get_attendance(
                student_id=student_id,
                subject=subject,
                start_date=date_from,
                end_date=date_to
            )
        else:
            return jsonify({"error": "student_id or class_id required"}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['student_id', 'student_name', 'class', 'subject', 'date', 'time', 'status'])
    writer.writeheader()
    writer.writerows(records)
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name='attendance_report.csv'
    )
