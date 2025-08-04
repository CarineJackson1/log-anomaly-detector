from flask import jsonify
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

# Function to register error handlers for the Flask application
def register_error_handlers(app):

    # Error handler for validation errors
    # This handler will catch validation errors raised by Marshmallow schemas.
    @app.errorhandler(ValidationError)
    def handle_validation_error(err):
        return jsonify({
            "status": "error",
            "message": "Invalid data",
            "details": err.messages
        }), 400

    # Error handler for integrity errors
    # This handler will catch integrity errors from SQLAlchemy, such as duplicate entries or constraint violations.
    # It returns a 400 status code with an error message.
    @app.errorhandler(IntegrityError)
    def handle_integrity_error(err):
        return jsonify({
            "status": "error",
            "message": "Database integrity error (duplicate or constraint violation)"
        }), 400

    # Error handler for 404 Not Found
    # This handler will catch requests to non-existent routes and return a 404 status code with an error message.
    @app.errorhandler(404)
    def not_found(err):
        return jsonify({
            "status": "error",
            "message": "Resource not found"
        }), 404

    # Error handler for 500 Internal Server Error
    # This handler will catch any unhandled exceptions in the application and return a 500 status code with an error message.
    # It is useful for debugging and logging unexpected errors.
    @app.errorhandler(500)
    def internal_server_error(err):
        return jsonify({
            "status": "error",
            "message": "Internal server error"
        }), 500
