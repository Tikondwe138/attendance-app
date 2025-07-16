# models/student_model.py

from database import db
import uuid
from datetime import datetime

class Student(db.Model):
    __tablename__ = 'students'

    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    student_id = db.Column(db.String, unique=True, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship to Attendance (bidirectional)
    attendance_records = db.relationship(
        "Attendance",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="select"
    )

    def __repr__(self):
        return f"<Student {self.student_id} - {self.full_name}>"
