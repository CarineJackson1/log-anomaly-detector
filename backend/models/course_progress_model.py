from enum import Enum
from sqlalchemy import Enum as SQLAlchemyEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from astroskill_lms_connector.backend.models.models import db
from datetime import datetime

class CompletionStatus(Enum):
    NOT_STARTED = "not_started"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"

class CourseProgress(db.Model):
    __tablename__ = 'course_progress'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    course_id: Mapped[int] = mapped_column(db.Integer, nullable=False)
    completion_status: Mapped[CompletionStatus] = mapped_column(
        SQLAlchemyEnum(CompletionStatus, name='completion_status_enum'), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    user = relationship("User", back_populates="course_progress")