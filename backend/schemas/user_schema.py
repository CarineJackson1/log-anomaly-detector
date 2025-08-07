from marshmallow import Schema, fields, validate, post_load
from backend.models.user_model import User, UserRole

# User schema for serialization and deserialization
# This schema defines the structure of user data for API requests and responses.
class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=validate.Length(min=3, max=50))
    email = fields.Email(required=True, validate=validate.Length(max=120))
    password = fields.Str(required=True, load_only=True, validate=validate.Length(min=6))
    role = fields.Str(
        required=False,
        validate=validate.OneOf([role.value for role in UserRole]),
        load_default=UserRole.LEARNER.value
    )
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)

    # This method is called after loading data to create a User instance.
    # It hashes the password and sets the role based on the provided value.
    @post_load
    def make_user(self, data, **kwargs):
        password = data.pop('password') # Extract the password for hashing
        role_value = data.pop('role', UserRole.LEARNER.value) # Default to LEARNER if not provided
        
        user = User(**data) # Create a User instance with the provided data
        user.role = UserRole(role_value) # Set the role using the UserRole enum
        user.set_password(password)  # Hash password
        return user
