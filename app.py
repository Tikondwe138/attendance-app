from flask import Flask, redirect, url_for
from database import db
from routes.attendance_routes import attendance_bp
from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.secret_key = 'super-secret-key'  # You should move this to an environment variable for production

    # --- Config ---
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- Init DB ---
    db.init_app(app)

    # --- Register Blueprints ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(attendance_bp)

    # --- Default Route ---
    @app.route('/')
    def home():
        return redirect(url_for('auth.login'))

    return app


if __name__ == "__main__":
    app = create_app()

    # Create DB tables before server starts
    with app.app_context():
        db.create_all()

    app.run(debug=True)
