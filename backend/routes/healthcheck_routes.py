from flask import Blueprint
from controllers.healthcheck_controller import get_health_status

# Define the Blueprint for health check routes
healthcheck_bp = Blueprint("healthcheck", __name__, url_prefix="/healthcheck")

# Define the health check route
@healthcheck_bp.route("/", methods=["GET"])
def healthcheck():
    return get_health_status()
