from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from utils.auth_decorators import roles_required

# Protected routes blueprint
protected_bp = Blueprint("protected", __name__, url_prefix="/protected")

# ----------------Protected route for any authenticated user
@protected_bp.get("/any-auth")
@jwt_required()
def any_auth():
    return jsonify({"status": "success", "message": "Any authenticated user OK"}), 200

# ----------------Protected route for employer role
@protected_bp.get("/employer-only")
@roles_required("employer")
def employer_only():
    return jsonify({"status": "success", "message": "Employer OK"}), 200

# ----------------Protected route for admin role
@protected_bp.get("/admin-only")
@roles_required("admin")
def admin_only():
    return jsonify({"status": "success", "message": "Admin OK"}), 200
