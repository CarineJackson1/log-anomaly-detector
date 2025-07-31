from flask import Flask
from config import DevelopmentConfig
from routes.healthcheck_routes import healthcheck_bp

# Create Flask application instance
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)

    # Register Blueprints
    app.register_blueprint(healthcheck_bp)

    @app.route("/")
    def home():
        return {"message": "AstroSkill LMS Connector Backend is running."}

    return app

# Run the application
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=5000)
