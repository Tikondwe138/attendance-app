from flask import Blueprint, render_template, request, jsonify
from models.attendance_model import init_db

attendance_bp = Blueprint('attendance', __name__)

@attendance_bp.route('/attendance')
def attendance():
    return render_template('attendance.html')

# Add more routes for attendance tracking and reporting as needed
