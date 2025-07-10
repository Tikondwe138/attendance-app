from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from functools import wraps
from models.user_model import validate_login

auth_bp = Blueprint('auth', __name__)

# --- Helper: Login required decorator ---
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user' not in session:
            flash("You need to log in first 😤", "error")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


# --- Login Route ---
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user_data = validate_login(username, password)
        if user_data:
            # Store both username and role in session
            session['user'] = user_data['username']
            session['role'] = user_data['role']
            flash(f"Welcome back, {user_data['username']} 🎉", 'success')
            return redirect(url_for('auth.profile'))
        else:
            flash('Invalid username or password 😬', 'error')

    return render_template('login.html')


# --- Profile Route ---
@auth_bp.route('/profile')
@login_required
def profile():
    username = session.get('user')
    role = session.get('role')
    return render_template('profile.html', user=username, role=role)


# --- Logout Route ---
@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully 👋', 'info')
    return redirect(url_for('auth.login'))
