from flask import Flask
from routes.attendance_routes import attendance_bp
from models.attendance_model import init_db

app = Flask(__name__)
app.register_blueprint(attendance_bp)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
