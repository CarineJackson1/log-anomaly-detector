from flask import Blueprint, jsonify, request
from schemas.user_schema import UserSchema
from models.user_model import User
from database import db

# Initialize the UserSchema for serialization and deserialization
# This schema will be used to validate and serialize user data in API requests and responses.
user_schema = UserSchema()

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

# Placeholder endpoints for future implementation
# login endpoint
@auth_bp.route('/login', methods=['POST'])
def login():
    return jsonify({"success": False, "message": "Login not yet implemented."}), 501

