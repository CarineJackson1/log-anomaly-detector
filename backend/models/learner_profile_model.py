from database import db
from datetime import datetime
from sqlalchemy.orm import relationship

class LearnerProfile(db.Model):
    __tablename__ = 'learner_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skills = db.Column(db.JSON, nullable=False)
    resume_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = relationship("User", back_populates="learner_profiles")