from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity
from schemas.user_schema import UserSchema
from schemas.login_schema import LoginSchema
from models.user_model import User
from database import db
from sqlalchemy.exc import IntegrityError
from utils.response_helpers import success_response
from enum import Enum

# Initialize the UserSchema for serialization and deserialization
# This schema will be used to validate and serialize user data in API requests and responses.
user_schema = UserSchema()

# Initialize the LoginSchema for user authentication
# This schema will be used to validate login credentials.
login_schema = LoginSchema()

# Create a Blueprint for authentication routes
auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

def _role_to_str(role) -> str:
    # Handles Enum and string roles
    if isinstance(role, Enum):
        return (role.value).lower()
    return (str(role) if role is not None else "").lower()

# Define routes for the authentication blueprint
# ------------- This route can be used to check if the auth service is running
@auth_bp.route('/', methods=['GET'])
def root():
    return success_response(message="Authentication routes are live and responding.")

# ---------------------- Health check endpoint
# Status endpoint to check if the auth service is operational
@auth_bp.route('/status', methods=['GET'])
def status():
    return success_response({
        "auth_status": "ready"
    })

# ---------------------- Registration endpoint to create a new user
# This endpoint expects a JSON payload with user details and creates a new user in the database.
@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    # Validate the incoming data using the UserSchema
    if User.query.filter_by(username=data.get('username')).first():
        return jsonify({"status": "error", "message": "Username already exists"}), 400
    if User.query.filter_by(email=data.get('email')).first():
        return jsonify({"status": "error", "message": "Email already exists"}), 400

    # Load the data into the UserSchema
    user = user_schema.load(data)
    # Add the new user to the database session
    db.session.add(user)

    # Attempt to commit the new user to the database
    # If there is an integrity error (e.g., duplicate entry), rollback the session and
    try:
        db.session.commit()
        return success_response(user_schema.dump(user), message="User registered successfully", status_code=201)
    except IntegrityError:
        db.session.rollback()
        return jsonify({"status": "error", "message": "User registration failed due to an integrity error."}), 400

# ---------------------- Login endpoint for user authentication
# This endpoint expects a JSON payload with email and password, verifies the credentials, and returns a JWT token if successful.
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    errors = login_schema.validate(data)
    # If there are validation errors, return them with a 400 status code.
    # This ensures that the input data meets the required format and constraints.
    if errors:
        return jsonify({"status": "error", "message": "Invalid input.", "details": errors}), 400

    # Find the user by email
    # If the user exists and the password is correct, create a JWT token.
    user = User.query.filter_by(email=data['email']).first()
    if user and user.check_password(data['password']):
        # Convert the user's role to a string for JWT claims
        role_str = _role_to_str(user.role)
        # Prepare additional claims for the JWT token
        additional_claims = {"role": role_str}  # "learner" / "employer" / "admin"
        # Create JWT token
        access_token = create_access_token(identity=user.id, additional_claims=additional_claims)
        # Return the token and user details in the response.
        # This allows the client to use the token for subsequent authenticated requests.
        return success_response({
            "access_token": access_token,
            "user": user_schema.dump(user)
        }, message="Login successful", status_code=200)
    else:
        # If the user does not exist or the password is incorrect, return an error message.
        # This ensures that the user receives feedback on why the login failed.
        return jsonify({"status": "error", "message": "Invalid email or password"}), 401

# ---------------------- Endpoint to get the current user's details
# This endpoint requires a valid JWT token and returns the user's information.
@auth_bp.route('/me', methods=['GET'])
# This route is protected by JWT authentication
# It ensures that only authenticated users can access their own details.
@jwt_required()
def get_current_user():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)
    # If the user is found, return their details.
    # This allows the client to retrieve their own user information securely.
    if not user:
        return jsonify({"status": "error", "message": "User not found"}), 404
    # Convert the user's role to a string for the response
    role_out = getattr(user.role, "value", str(user.role)).lower() if user.role else "learner"
    # Serialize the user data using the UserSchema
    # This ensures that the response format is consistent and includes only the necessary fields.
    return success_response({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "role": role_out
    }, message="User retrieved successfully")
