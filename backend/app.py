from flask import Flask, jsonify
from flask_cors import CORS
from config import DevelopmentConfig
from routes.healthcheck_routes import healthcheck_bp
from routes.auth_routes import auth_bp

# Create Flask application instance
def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/auth/*": {"origins": "*"}})
    
    app.config.from_object(DevelopmentConfig)

    # Register Blueprints
    app.register_blueprint(healthcheck_bp)
    app.register_blueprint(auth_bp)
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"status": "error", "message": "Route not found"}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({"status": "error", "message": "Internal server error"}), 500

    @app.route("/")
    def home():
        return {"message": "AstroSkill LMS Connector Backend is running."}

    return app

# Run the application
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
