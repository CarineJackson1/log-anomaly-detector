from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import DevelopmentConfig
from routes.healthcheck_routes import healthcheck_bp
from database import db, init_db
from routes.auth_routes import auth_bp

# Create Flask application instance
def create_app():
    app = Flask(__name__)
    
    CORS(app, resources={r"/auth/*": {"origins": "*"}})
    
    # Configure the application with development settings
    app.config.from_object(DevelopmentConfig)
    
    # JWT configuration
    # This secret key should be kept secure and not hardcoded in production.
    app.config['JWT_SECRET_KEY'] = 'your-secret-key'  # This will be replaced with a secure env variable
    # Initialize JWT Manager
    # This manager will handle JWT creation and verification.
    jwt = JWTManager(app)
    
    # Initialize the database
    init_db(app)
    
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
    
    @app.route("/db-check")
    def db_check():
        return {"tables": db.inspect(db.engine).get_table_names()}


    return app
    


# Run the application
if __name__ == "__main__":
    app = create_app()
    
    # Prints the current database tables for debugging
    with app.app_context():
        # This line can be used to verify that the database is initialized correctly.
        print(db.inspect(db.engine).get_table_names())
    
    app.run(host="0.0.0.0", port=5000)
