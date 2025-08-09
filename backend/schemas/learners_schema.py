from marshmallow import Schema, fields, validate, validates, ValidationError, post_load
from backend.models.learner_profile_model import LearnerProfile

class LearnerProfileSchema(Schema):
    id = fields.Int(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    user_id = fields.Int(required=True)
    skills = fields.List(fields.Str(validate=validate.Length(min=1)), required=True)
    resume_url = fields.Url(required=True, schemes={"http", "https"}, validate=validate.Length(max=500))
    
    @validates("skills")
    def validate_skills(self, value):
        # Ensure strings & no case-insensitive duplicates
        cleaned = [s.strip() for s in value if isinstance(s, str)]
        if len(cleaned) != len(value):
            raise ValidationError("All skills must be strings.")
        if len(set(map(str.lower, cleaned)) != len(cleaned)):
            raise ValidationError("Duplicate skills are not allowed.")
        
    @post_load
    def make_learner_profile(self, data, **kwargs):
        # Build a LearnerProfile instance on load (useful for POST)
        return LearnerProfile(**data)