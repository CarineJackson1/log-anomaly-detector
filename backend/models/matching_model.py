from datetime import datetime
from database import db
from sqlalchemy import UniqueConstraint
import enum

# This class represents the matching data between learners and job postings.
class MatchingData(db.Model):
    __tablename__ = "matching_data"
    __table_args__ = (
        UniqueConstraint("learner_profile_id", "job_posting_id", name="uq_matching_learner_job"),
    )

    id = db.Column(db.Integer, primary_key=True)
    learner_profile_id = db.Column(
        db.Integer,
        db.ForeignKey("learner_profiles.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    job_posting_id = db.Column(
        db.Integer,
        db.ForeignKey("job_postings.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )
    score = db.Column(db.Numeric(5, 2), nullable=False)  # 0–100.00
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    learner = db.relationship("LearnerProfile", back_populates="matchings")
    job_posting = db.relationship("JobPosting", back_populates="matchings")

    def __repr__(self):
        return f"<MatchingData(learner_profile_id={self.learner_profile_id}, job_posting_id={self.job_posting_id}, score={self.score})>"
