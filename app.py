from flask import Flask, render_template
from routes.attendance_routes import attendance_bp
from routes.auth_routes import auth_bp  # import your new login routes
from models.attendance_model import db  # SQLAlchemy instance

app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Needed for session management

# Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize DB
db.init_app(app)

# Register Blueprints
app.register_blueprint(attendance_bp)
app.register_blueprint(auth_bp)

# Default route
@app.route('/')
def home():
    return render_template('login.html', hide_navbar=True)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
