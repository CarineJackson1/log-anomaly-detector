from flask import Flask
from config import DevelopmentConfig
from routes.healthcheck_routes import healthcheck_bp
from database import db, init_db

# Create Flask application instance
def create_app():
    app = Flask(__name__)
    app.config.from_object(DevelopmentConfig)
    
    # Initialize the database
    init_db(app)
    
    # Register Blueprints
    app.register_blueprint(healthcheck_bp)

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
