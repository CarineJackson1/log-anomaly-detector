from datetime import datetime
from database import db
import enum

# This enum defines the different sources a course can originate from.
class CourseSource(enum.Enum):
    MOODLE = "moodle"
    INTERNAL = "internal"

# This class represents a course in the system.
class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    # If the course comes from Moodle, store its external id as a reference
    moodle_course_id = db.Column(db.Integer, nullable=True, index=True, unique=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    source = db.Column(
        db.Enum(CourseSource, name="course_source_enum", native_enum=False),
        nullable=False,
        default=CourseSource.MOODLE,
        )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    enrollments = db.relationship("Enrollment", back_populates="course", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Course(id={self.id}, title='{self.title}', source='{self.source}')>"
