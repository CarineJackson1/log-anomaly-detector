from marshmallow import Schema, fields, validate

# Login schema for user authentication
# This schema defines the structure of login data for API requests.
class LoginSchema(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True, validate=validate.Length(min=6))
