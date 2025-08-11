from datetime import datetime
from database import db

# This class represents a job posting in the system.
class JobPosting(db.Model):
    __tablename__ = "job_postings"

    id = db.Column(db.Integer, primary_key=True)
    employer_id = db.Column(
        db.Integer,
        db.ForeignKey("employers.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    requirements = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    employer = db.relationship("Employer", back_populates="job_postings")
    applications = db.relationship("Application", back_populates="job_posting", cascade="all, delete-orphan")
    matchings = db.relationship("MatchingData", back_populates="job_posting", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<JobPosting(id={self.id}, title='{self.title}')>"
