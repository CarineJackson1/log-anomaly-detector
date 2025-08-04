from flask import jsonify

# Utility function to create a standardized success response
# This function can be used across different endpoints to maintain consistency in API responses.
def success_response(data=None, message="Success", status_code=200):
    """
    Standardized success response for API endpoints.
    """
    response = {
        "status": "success",
        "message": message
    }
    # If data is provided, include it in the response
    # This allows for flexibility in returning different types of data.
    if data is not None:
        response["data"] = data
    
    # Return the response as JSON with the specified status code
    # This ensures that the client receives a well-structured response.
    return jsonify(response), status_code
