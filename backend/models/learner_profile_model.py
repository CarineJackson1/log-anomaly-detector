from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship
from datetime import datetime
from astroskill_lms_connector.backend.models.models import db
from typing import List

class LearnerProfile(db.Model):
    __tablename__ = 'learner_profiles'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    skills: Mapped[List[str]] = mapped_column(JSON, nullable=False)
    resume_url: Mapped[str] = mapped_column(db.String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="learner_profiles")