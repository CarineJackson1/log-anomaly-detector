from datetime import datetime
from database import db
from sqlalchemy import UniqueConstraint

# This enum defines the different statuses an application can have.
application_status_enum = db.Enum(
    "pending", "accepted", "rejected",
    name="application_status_enum"
)

# This class represents an application for a job posting in the system.
class Application(db.Model):
    __tablename__ = "applications"
    __table_args__ = (
        UniqueConstraint("learner_profile_id", "job_posting_id", name="uq_application_learner_job"),
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
    status = db.Column(application_status_enum, nullable=False, server_default="pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    learner = db.relationship("LearnerProfile", back_populates="applications")
    job_posting = db.relationship("JobPosting", back_populates="applications")

    def __repr__(self):
        return f"<Application(learner_profile_id={self.learner_profile_id}, job_posting_id={self.job_posting_id}, status={self.status})>"
