from datetime import datetime
from database import db
from sqlalchemy import UniqueConstraint, Enum as SQLEnum

# This enum defines the different statuses an enrollment can have.
enrollment_status_enum = db.Enum('active', 'completed', 'dropped', name='enrollment_status_enum')

# This class represents an enrollment in a course.
class Enrollment(db.Model):
    __tablename__ = 'enrollments'
    __table_args__ = (
        UniqueConstraint('learner_profile_id', 'course_id', name='uq_enrollment_learner_course'),
    )

    id = db.Column(db.Integer, primary_key=True)
    learner_profile_id = db.Column(
        db.Integer,
        db.ForeignKey('learner_profiles.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    course_id = db.Column(
        db.Integer,
        db.ForeignKey('courses.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    status = db.Column(enrollment_status_enum, nullable=False, server_default='active')
    progress = db.Column(db.Numeric(5, 2), nullable=False, server_default='0.00')  # 0–100.00
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # Relationships
    learner = db.relationship("LearnerProfile", back_populates="enrollments")
    course = db.relationship("Course", back_populates="enrollments")

    def __repr__(self):
        return f"<Enrollment(learner_profile_id={self.learner_profile_id}, course_id={self.course_id}, status={self.status})>"
