from datetime import datetime
from database import db
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLAlchemyEnum
from enum import Enum

class CompletionStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    
class CourseProgress(db.Model):
    __tablename__ = 'course_progress'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    course_id = db.Column(db.Integer, nullable=False)
    completion_status = db.Column(
        SQLAlchemyEnum(CompletionStatus, name='completion_status_enum'), nullable=False
    )
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User")