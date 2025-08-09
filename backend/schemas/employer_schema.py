from marshmallow import Schema, fields, validate, validates, ValidationError

# Full read schema (for GET responses)
class EmployerSchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(required=True)
    company_name = fields.Str(required=True, validate=validate.Length(min=1, max=500))
    # Store as JSON in DB; expose as a list of strings in the API
    interest_tags = fields.List(fields.Str(validate=validate.Length(min=1)), allow_none=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates("interest_tags")
    def validate_interest_tags(self, value):
        # Ensure unique, trimmed tags (OPTIONAL)
        cleaned = [t.strip() for t in value if isinstance(t, str)]
        if len(cleaned) != len(value):
            raise ValidationError("All interest_tags must be strings.")
        if len(set(map(str.lower, cleaned))) != len(cleaned):
            raise ValidationError("Duplicate tags are not allowed.")
        
