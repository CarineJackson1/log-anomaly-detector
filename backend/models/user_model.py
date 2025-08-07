from backend.database import db
from datetime import datetime
from passlib.hash import bcrypt # type: ignore
import enum

# Setting User Roles for Learner, Employer, and Admin
# This enum defines the different roles a user can have in the system.
class UserRole(enum.Enum):
    LEARNER = 'learner'
    EMPLOYER = 'employer'
    ADMIN = 'admin'

# User model for the application
# This model represents the users in the system, including their credentials and timestamps.
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum(UserRole), nullable=False, default=UserRole.LEARNER)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    learner_profiles = db.relationship("LearnerProfile", back_populates="user", cascade="all, delete-orphan")
    course_progress = db.relationship("CourseProgress", back_populates="user", cascade="all, delete-orphan")
    employer = db.relationship("Employer", back_populates="user", cascade="all, delete-orphan")
    
    # This method sets the user's password hash using bcrypt for secure storage.
    # It hashes the provided password and stores it in the password_hash field.
    def set_password(self, password):
        """Set the user's password hash."""
        self.password_hash = bcrypt.hash(password)
    
    # This method checks if the provided password matches the stored hash.
    # It uses bcrypt for secure password hashing and verification.    
    def check_password(self, password):
        """Check the user's password against the stored hash."""
        return bcrypt.verify(password, self.password_hash)
    
    # This method returns a string representation of the user object.
    # It is useful for debugging and logging purposes.
    def __repr__(self):
        return f"<User {self.username}>"
