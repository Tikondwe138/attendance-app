from flask import Blueprint, render_template, request, jsonify, send_file
from models.attendance_model import init_db, mark_attendance, get_attendance
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
        mark_attendance(
            data['student_id'],
            data['subject'],
            data['date'],
            data['time'],
            data['status']
        )
        return jsonify({"message": "Attendance marked successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@attendance_bp.route('/api/attendance/report', methods=['GET'])
def attendance_report():
    student_id = request.args.get('student_id')
    date = request.args.get('date')
    subject = request.args.get('subject')
    records = get_attendance(student_id, date, subject)
    return jsonify(records)

@attendance_bp.route('/api/attendance/export/csv', methods=['GET'])
def export_attendance_csv():
    student_id = request.args.get('student_id')
    date = request.args.get('date')
    subject = request.args.get('subject')
    records = get_attendance(student_id, date, subject)
    output = io.StringIO()
    writer = csv.DictWriter(output, fieldnames=['student_id', 'subject', 'date', 'time', 'status'])
    writer.writeheader()
    writer.writerows(records)
    output.seek(0)
    return send_file(io.BytesIO(output.getvalue().encode()), mimetype='text/csv', as_attachment=True, download_name='attendance_report.csv')

# Add more routes for attendance tracking and reporting as needed
