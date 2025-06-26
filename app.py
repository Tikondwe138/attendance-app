from flask import Flask, render_template
from routes.attendance_routes import attendance_bp
from models.attendance_model import init_db
import os

app = Flask(__name__, template_folder='templates', static_folder='static')

# Register attendance blueprint under /api/attendance (as per your attendance_routes)
app.register_blueprint(attendance_bp, url_prefix='/api/attendance')

# Login page (default route)
@app.route('/')
@app.route('/login')
def login():
    return render_template('login.html')

# Profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

# Attendance page (main attendance UI)
@app.route('/attendance')
def attendance():
    return render_template('attendance.html')

if __name__ == "__main__":
    # Initialize DB only if it doesn't exist (creates tables, etc)
    if not os.path.exists('attendance.db'):
        init_db()
    app.run(debug=True)
