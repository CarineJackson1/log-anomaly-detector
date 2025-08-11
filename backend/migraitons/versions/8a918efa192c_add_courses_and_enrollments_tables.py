from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "8a918efa192c"
down_revision = "6f41a01df0aa"
branch_labels = None
depends_on = None

# This migration adds the courses and enrollments tables with appropriate constraints and relationships.
def upgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name
    is_postgres = dialect == "postgresql"

    # Choose column types per dialect
    course_source_coltype = sa.Enum("moodle", "internal", name="course_source_enum") if is_postgres else sa.String(32)
    enrollment_status_coltype = sa.Enum("active", "completed", "dropped", name="enrollment_status_enum") if is_postgres else sa.String(32)

    # Create real enum types only on Postgres
    if is_postgres:
        op.execute("CREATE TYPE course_source_enum AS ENUM ('moodle','internal')")
        op.execute("CREATE TYPE enrollment_status_enum AS ENUM ('active','completed','dropped')")

    # ----- courses -----
    courses_cols = [
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("moodle_course_id", sa.Integer, nullable=True),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("source", course_source_coltype, nullable=False, server_default="moodle"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
    ]

    # Inline CHECK for SQLite (no ALTER)
    if not is_postgres:
        courses_cols.append(sa.CheckConstraint("source IN ('moodle','internal')", name="ck_courses_source_enum"))

    op.create_table("courses", *courses_cols)
    op.create_index("ix_courses_moodle_course_id", "courses", ["moodle_course_id"], unique=True)

    # ----- enrollments -----
    enrollments_cols = [
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("learner_profile_id", sa.Integer, sa.ForeignKey("learner_profiles.id", ondelete="CASCADE"), nullable=False),
        sa.Column("course_id", sa.Integer, sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False),
        sa.Column("status", enrollment_status_coltype, nullable=False, server_default="active"),
        sa.Column("progress", sa.Numeric(5, 2), nullable=False, server_default="0.00"),
        sa.Column("created_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.Column("updated_at", sa.DateTime(), nullable=False, server_default=sa.text("CURRENT_TIMESTAMP")),
        sa.UniqueConstraint("learner_profile_id", "course_id", name="uq_enrollment_learner_course"),
    ]

    if not is_postgres:
        enrollments_cols.append(sa.CheckConstraint("status IN ('active','completed','dropped')", name="ck_enrollments_status_enum"))

    op.create_table("enrollments", *enrollments_cols)
    op.create_index("ix_enrollments_learner_profile_id", "enrollments", ["learner_profile_id"])
    op.create_index("ix_enrollments_course_id", "enrollments", ["course_id"])

# This function removes the courses and enrollments tables and their associated constraints.
def downgrade():
    bind = op.get_bind()
    dialect = bind.dialect.name
    is_postgres = dialect == "postgresql"

    op.drop_index("ix_enrollments_course_id", table_name="enrollments")
    op.drop_index("ix_enrollments_learner_profile_id", table_name="enrollments")
    op.drop_table("enrollments")

    op.drop_index("ix_courses_moodle_course_id", table_name="courses")
    op.drop_table("courses")

    if is_postgres:
        op.execute("DROP TYPE enrollment_status_enum")
        op.execute("DROP TYPE course_source_enum")
