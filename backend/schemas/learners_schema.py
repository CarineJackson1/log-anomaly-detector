from marshmallow import Schema, fields, validate, validates, ValidationError, post_load, EXCLUDE
from models.learner_profile_model import LearnerProfile

class LearnerProfileSchema(Schema):
    class Meta:
        unknown = EXCLUDE # ignores unexpected fields on load
        
    id = fields.Int(dump_only=True)
    # This field is load_only to prevent it from being included in responses
    user_id = fields.Int(load_only=True)
    skills = fields.List(
                        fields.Str(validate=validate.Length(min=1)), 
                        required=True,
                        validate=validate.Length(min=1, max=100), # List must have at least 1 and at most 100 skills
                        )
    resume_url = fields.Url(
                        required=True, 
                        schemes={"http", "https"}, 
                        validate=validate.Length(max=500)
                        )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates("skills")
    def validate_skills(self, value, **kwargs):
        # all must be strings
        if any(not isinstance(s, str) for s in value):
            raise ValidationError("All skills must be strings.")
        # no blank after trim
        trimmed = [s.strip() for s in value]
        if any(len(s) == 0 for s in trimmed):
            raise ValidationError("Skills cannot be blank.")
        # no case-insensitive duplicates
        if len(set(map(str.lower, trimmed))) != len(trimmed):
            raise ValidationError("Duplicate skills are not allowed (case-insensitive).")
        
    @post_load
    def make_learner_profile(self, data, **kwargs):
        # Build a LearnerProfile instance on load (useful for POST)
        return LearnerProfile(**data)