from flask import Blueprint, request, jsonify
from app.models import User

data_blueprint = Blueprint("data", __name__)


@data_blueprint.route("/upload_data", methods=["POST"])
def upload_data():
    """
    Uploads interaction data for a specific user.
    """
    data = request.get_json()

    if (
        not data
        or "user_id" not in data
        or "timestamp" not in data
        or "data" not in data
    ):
        return jsonify({"error": "user_id, timestamp, and data are required."}), 400

    user_id = data["user_id"]
    timestamp = data["timestamp"]
    interaction_data = data["data"]

    # Check if the user exists
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Mock saving data logic
    print(f"Interaction data for user {user_id} at {timestamp}: {interaction_data}")

    return jsonify({"message": "Data uploaded successfully."}), 200
