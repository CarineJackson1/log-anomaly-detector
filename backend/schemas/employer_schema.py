from marshmallow import Schema, fields, validate, validates, ValidationError, EXCLUDE

# Full read schema (for GET responses)
class EmployerSchema(Schema):
    class Meta:
        unknown = EXCLUDE
        
    id = fields.Int(dump_only=True)
    # This field is load_only to prevent it from being included in responses
    user_id = fields.Int(load_only=True)
    company_name = fields.Str(
                        required=True, 
                        validate=validate.Length(min=1, max=500))
    # Store as JSON in DB; expose as a list of strings in the API
    interest_tags = fields.List(
                        fields.Str(validate=validate.Length(min=1)), 
                        allow_none=True) # Optional field
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    
    @validates("interest_tags")
    def validate_interest_tags(self, value, **kwargs):
        # None means the field is intentionally omitted or null — allowed
        if value is None:
            return

        # Must be strings
        if any(not isinstance(t, str) for t in value):
            raise ValidationError("All interest_tags must be strings.")

        trimmed = [t.strip() for t in value]

        # Reject if any string is empty after trimming
        if any(len(t) == 0 for t in trimmed):
            raise ValidationError("interest_tags cannot contain blank values.")

        # Reject duplicates (case-insensitive)
        if len(set(map(str.lower, trimmed))) != len(trimmed):
            raise ValidationError("Duplicate interest_tags are not allowed (case-insensitive).")
        
