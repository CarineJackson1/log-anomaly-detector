from flask import Blueprint
from flask import jsonify

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/status', methods=['GET'])
def status():
    return jsonify({
        "status": "auth routes ready",
        "message": "Authentication blueprint is live."
    }), 200