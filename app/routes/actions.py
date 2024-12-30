from flask import Blueprint, request, jsonify
from app.models import User

actions_blueprint = Blueprint("actions", __name__)


@actions_blueprint.route("/actions", methods=["POST"])
def request_action():
    """
    Requests an action for a specific user based on context.
    """
    data = request.get_json()

    if not data or "user_id" not in data or "timestamp" not in data:
        return jsonify({"error": "user_id and timestamp are required."}), 400

    user_id = data["user_id"]
    context = data.get("context", {})

    # Check if the user exists
    user = User.query.filter_by(user_id=user_id).first()
    if not user:
        return jsonify({"error": "User not found."}), 404

    # Mock action response (update with actual RL algorithm logic)
    action = {"action_type": "click", "context": context}

    return jsonify({"user_id": user_id, "action": action}), 200
