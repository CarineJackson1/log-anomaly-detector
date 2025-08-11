from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

# Role-based access control decorator
def roles_required(*allowed_roles):
    """
    Usage:
        @roles_required("admin")
        @roles_required("employer", "admin")
        @roles_required("learner", "employer")  # admin is always allowed implicitly
    """
    # Normalize allowed roles to lowercase
    allowed = {r.lower() for r in allowed_roles}

    # Decorator to wrap the actual route function
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            # 401 if no/invalid token
            verify_jwt_in_request()
            claims = get_jwt()
            role = (claims.get("role") or "").lower()

            # Admin override: admin may access all routes
            if role == "admin":
                return fn(*args, **kwargs)

            if role in allowed:
                return fn(*args, **kwargs)

            return jsonify({
                "status": "error",
                "message": "Forbidden: insufficient role",
                "details": {"required": sorted(list(allowed)), "actual": role}
            }), 403
        return decorator
    return wrapper
