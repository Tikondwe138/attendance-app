# models/attendance_model.py

from database import db

class Attendance(db.Model):
    __tablename__ = 'attendance'

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(
        db.String,
        db.ForeignKey('students.student_id', ondelete="CASCADE"),
        nullable=False
    )
    subject = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    status = db.Column(db.String(20), nullable=False)

    # Relationship to Student model (bidirectional)
    student = db.relationship(
        "Student",
        back_populates="attendance_records",
        lazy="joined"
    )

    def __repr__(self):
        return f"<Attendance {self.student_id} - {self.subject} on {self.date}>"
