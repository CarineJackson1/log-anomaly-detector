import pytest
from marshmallow import ValidationError
from schemas.learners_schema import LearnerProfileSchema
from schemas.employer_schema import EmployerSchema
from schemas.course_progress_schema import CourseProgressSchema
from models.course_progress_model import CompletionStatus

def getf(obj, name):
    """Return field `name` from a dict or a model instance."""
    return getattr(obj, name) if hasattr(obj, name) else obj[name]

def test_learner_profile_schema_valid():
    data = {"skills": ["Python", "Flask"], "resume_url": "https://ex.com/cv.pdf"}
    out = LearnerProfileSchema().load(data)
    assert getf(out, "skills") == ["Python", "Flask"]

def test_learner_profile_schema_invalid_dups():
    with pytest.raises(ValidationError):
        LearnerProfileSchema().load({"skills": ["Python", "python"], "resume_url": "https://ex.com/cv.pdf"})

def test_employer_schema_valid():
    data = {"company_name": "Astro Corp", "interest_tags": ["Aerospace", "AI"]}
    out = EmployerSchema().load(data)
    assert getf(out, "company_name") == "Astro Corp"

def test_employer_schema_invalid_blank_tag():
    with pytest.raises(ValidationError):
        EmployerSchema().load({"company_name": "X", "interest_tags": ["  "]})

def test_course_progress_schema_defaults():
    out = CourseProgressSchema().load({"user_id": 1, "course_id": 10})
    assert getf(out, "completion_status") in ("not_started", "NOT_STARTED")

def test_course_progress_schema_bad_enum():
    with pytest.raises(ValidationError):
        CourseProgressSchema().load({"user_id": 1, "course_id": 10, "completion_status": "done"})
