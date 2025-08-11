from database import db
from datetime import datetime
from sqlalchemy.orm import relationship

# LearnerProfile model to represent learner profiles in the system
class LearnerProfile(db.Model):
    __tablename__ = 'learner_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skills = db.Column(db.JSON, nullable=False)
    resume_url = db.Column(db.String(500), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Establishing relationships with other models
    user = relationship("User", back_populates="learner_profiles")
    enrollments = relationship("Enrollment", back_populates="learner", cascade="all, delete-orphan")
    applications = relationship("Application", back_populates="learner", cascade="all, delete-orphan")
    matchings = relationship("MatchingData", back_populates="learner", cascade="all, delete-orphan")

    # This method provides a string representation of the LearnerProfile instance
    def __repr__(self):
        return f"<LearnerProfile(id={self.id}, user_id={self.user_id}, skills={self.skills}, resume_url='{self.resume_url}', created_at={self.created_at}, updated_at={self.updated_at})>"