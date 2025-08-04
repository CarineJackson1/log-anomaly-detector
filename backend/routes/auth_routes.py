from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token
from schemas.user_schema import UserSchema
from schemas.login_schema import LoginSchema
from models.user_model import User
from database import db

# Initialize the UserSchema for serialization and deserialization
# This schema will be used to validate and serialize user data in API requests and responses.
user_schema = UserSchema()

# Initialize the LoginSchema for user authentication
# This schema will be used to validate login credentials.
login_schema = LoginSchema()

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

# Define routes for the authentication blueprint
# This route can be used to check if the auth service is running
@auth_bp.route('/', methods=['GET'])
def root():
    return jsonify({
        "success": True,
        "data": {"auth_status": "ready"},
        "message": "Authentication blueprint is active."
    }), 200

# Status endpoint to check if the auth service is operational
@auth_bp.route('/status', methods=['GET'])
def status():
    return jsonify({
        "success": True,
        "data": {"auth_status": "ready"},
        "message": "Authentication routes are live and responding."
    }), 200
    
# Registration endpoint to create a new user
# This endpoint expects a JSON payload with user details and creates a new user in the database.
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user = user_schema.load(data)
    db.session.add(user)
    db.session.commit()
    return user_schema.jsonify(user), 201

# Login endpoint for user authentication
# This endpoint expects a JSON payload with email and password, verifies the credentials, and returns a JWT token if successful.
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    # If there are validation errors, return them with a 400 status code.
    # This ensures that the input data meets the required format and constraints.
    if errors:
        return jsonify(errors), 400

    # Find the user by email
    # If the user exists and the password is correct, create a JWT token.
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        # Create JWT token
        access_token = create_access_token(identity=user.id)
        # Return the token and user details in the response.
        # This allows the client to use the token for subsequent authenticated requests.
        return jsonify({
            "access_token": access_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role.value
            }
        }), 200
    else:
        # If the user does not exist or the password is incorrect, return an error message.
        # This ensures that the user receives feedback on why the login failed.
        return jsonify({"error": "Invalid email or password"}), 401

