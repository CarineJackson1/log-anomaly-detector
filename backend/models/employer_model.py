from sqlalchemy import ForeignKey, JSON
from sqlalchemy.orm import relationship, Mapped, mapped_column
from datetime import datetime
from astroskill_lms_connector.backend.models.models import db
from typing import Optional, List

class Employer(db.Model):
    __tablename__ = 'employers'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), nullable=False)
    company_name: Mapped[str] = mapped_column(db.String(500), nullable=False)
    interest_tags: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(db.DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="employers")