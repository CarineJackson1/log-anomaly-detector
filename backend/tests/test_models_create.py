from database import db
from app import create_app
from models.user_model import User, UserRole
from models.learner_profile_model import LearnerProfile
from models.employer_model import Employer
from models.course_progress_model import CourseProgress, CompletionStatus

def test_create_core_entities(tmp_path):
    app = create_app()
    with app.app_context():
        # create a user
        u = User(username="u1", email="u1@example.com", role=UserRole.LEARNER)
        u.set_password("Password123!")
        db.session.add(u)
        db.session.commit()

        # learner profile
        lp = LearnerProfile(user_id=u.id, skills=["Python"], resume_url="https://ex.com/cv.pdf")
        db.session.add(lp)

        # employer tied to same user (if you allow dual roles; otherwise create a second user)
        e = Employer(user_id=u.id, company_name="Astro Corp", interest_tags=["AI"])
        db.session.add(e)

        # course progress
        cp = CourseProgress(user_id=u.id, course_id=101, completion_status=CompletionStatus.NOT_STARTED)
        db.session.add(cp)

        db.session.commit()

        assert lp.id is not None
        assert e.id is not None
        assert cp.id is not None

        # verify relationships
        assert lp.user.id == u.id
        assert e.user.id == u.id
