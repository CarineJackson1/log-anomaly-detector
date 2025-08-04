from marshmallow import Schema, fields, validate, post_load
from models.user_model import User, UserRole

# User schema for serialization and deserialization
# This schema defines the structure of user data for API requests and responses.
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    role = fields.Str(
        required=False,
        validate=validate.OneOf([role.value for role in UserRole]),
        missing=UserRole.LEARNER.value
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # This method is called after deserialization to convert the role string to UserRole enum
    # and create a User instance.
    @post_load
    def make_user(self, data, **kwargs):
        if 'role' in data and isinstance(data['role'], str):
            data['role'] = UserRole(data['role'])
        return User(**data)
