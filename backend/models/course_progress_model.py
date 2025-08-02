from datetime import datetime
from database import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum

# SQLAlchemy Enum setup for cycle through completion status

class CompletionStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

# CourseProgress model to track user progress in courses
class CourseProgress(db.Model):
    __tablename__ = 'course_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    completion_status = db.Column(
        SQLAlchemyEnum(CompletionStatus, name='completion_status_enum'), 
        nullable=False,
        default=CompletionStatus.NOT_STARTED
    )
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", backref=db.backref("course_progress", cascade="all, delete"))
    course = relationship("Course", backref=db.backref("course_progress", cascade="all, delete"))
    
    # This method provides a string representation of the CourseProgress instance
    def __repr__(self):
        return f"<CourseProgress(user_id={self.user_id}, course_id={self.course_id}, completion_status={self.completion_status.value}, updated_at={self.updated_at})>"