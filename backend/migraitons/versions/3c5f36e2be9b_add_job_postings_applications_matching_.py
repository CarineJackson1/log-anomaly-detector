"""Add job_postings, applications, matching_data

Revision ID: 3c5f36e2be9b
Revises: 826b0ba6e268
Create Date: 2025-08-11 01:44:33.290301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3c5f36e2be9b'
down_revision: Union[str, Sequence[str], None] = '826b0ba6e268'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # job_postings
    op.create_table(
        "job_postings",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("employer_id", sa.Integer, sa.ForeignKey("employers.id", ondelete="CASCADE"), nullable=False),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("requirements", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    )
    op.create_index("ix_job_postings_employer_id", "job_postings", ["employer_id"])

    # applications (with enum-like CHECK)
    op.create_table(
        "applications",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("learner_profile_id", sa.Integer, sa.ForeignKey("learner_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_posting_id", sa.Integer, sa.ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", sa.String(32), nullable=False, server_default="pending"),
        sa.CheckConstraint("status IN ('pending','accepted','rejected')", name="ck_applications_status_enum"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("learner_profile_id", "job_posting_id", name="uq_application_learner_job"),
    )
    op.create_index("ix_applications_learner_profile_id", "applications", ["learner_profile_id"])
    op.create_index("ix_applications_job_posting_id", "applications", ["job_posting_id"])

    # matching_data
    op.create_table(
        "matching_data",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("learner_profile_id", sa.Integer, sa.ForeignKey("learner_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("job_posting_id", sa.Integer, sa.ForeignKey("job_postings.id", ondelete="CASCADE"), nullable=False),
        sa.Column("score", sa.Numeric(5, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("learner_profile_id", "job_posting_id", name="uq_matching_learner_job"),
    )
    op.create_index("ix_matching_learner_profile_id", "matching_data", ["learner_profile_id"])
    op.create_index("ix_matching_job_posting_id", "matching_data", ["job_posting_id"])

def downgrade():
    op.drop_index("ix_matching_job_posting_id", table_name="matching_data")
    op.drop_index("ix_matching_learner_profile_id", table_name="matching_data")
    op.drop_table("matching_data")

    op.drop_index("ix_applications_job_posting_id", table_name="applications")
    op.drop_index("ix_applications_learner_profile_id", table_name="applications")
    op.drop_table("applications")

    op.drop_index("ix_job_postings_employer_id", table_name="job_postings")
    op.drop_table("job_postings")
