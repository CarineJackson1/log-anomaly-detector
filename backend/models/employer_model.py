from datetime import datetime
from database import db
from sqlalchemy.orm import relationship

# Employer model to represent employers in the system
class Employer(db.Model):
    __tablename__ = 'employers'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    company_name = db.Column(db.String(500), nullable=False)
    interest_tags = db.Column(db.JSON, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Establishing relationships with other models
    user = relationship("User", back_populates="employer")
    job_postings = relationship("JobPosting", back_populates="employer", cascade="all, delete-orphan")
    
    # This method provides a string representation of the Employer instance
    def __repr__(self):
        return f"<Employer(id={self.id}, user_id={self.user_id}, company_name='{self.company_name}', created_at={self.created_at}, updated_at={self.updated_at})>"