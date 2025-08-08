from flask import jsonify

# Controller for health check routes
def get_health_status():
    return jsonify({"status": "success", "message": "Backend is healthy"}), 200
