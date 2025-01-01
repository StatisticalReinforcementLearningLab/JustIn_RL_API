import logging
import datetime
from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models import User, Action, ModelParameters

action_blueprint = Blueprint("action", __name__)


def check_fields(data: dict) -> tuple[bool, str]:
    """
    Check if the required fields are present in the data.
    """
    if not data or "user_id" not in data or "timestamp" not in data:
        return False, "user_id and timestamp are required."

    if "context" not in data:
        return False, "context is required."

    if "temperature" not in data["context"]:
        return False, "Invalid context. Temperature is required."

    return True, ""


@action_blueprint.route("/action", methods=["POST"])
def request_action():
    """
    Requests an action for a specific user based on context.
    Currently assumes that the context is only temperature.
    """
    try:
        data = request.get_json()

        # Check if the required fields are present
        fields_present, error_message = check_fields(data)
        if not fields_present:
            return jsonify({"error": error_message}), 400

        # Extract the data
        user_id = data["user_id"]
        context = data["context"]
        request_timestamp = data["timestamp"]
        received_timestamp_iso = datetime.datetime.now().isoformat()

        # Check if the user exists
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"error": "User not found."}), 404

        # Get the RL algorithm
        rl_algorithm = current_app.rl_algorithm

        # Make the state
        state = rl_algorithm.make_state(context)

        # Get the latest model parameters from the database
        model_parameters = ModelParameters.query.order_by(
            ModelParameters.created_at.desc()
        ).first()

        # Check if the model parameters exist
        if not model_parameters:
            return jsonify({"error": "Model parameters not found."}), 404

        # Extract the model parameters, in this case, the probability
        probability = model_parameters.probability

        # Get the action, action selection probability, and random state 
        # used to generate the action
        action, prob, random_state = rl_algorithm.get_action(
            user_id, state, {"probability": probability}
        )

        # Save the action to the action database
        new_action = Action(
            user_id=user_id,
            action=action,
            state=state,
            raw_context=context,
            action_prob=prob,
            random_state=random_state,
            request_timestamp=request_timestamp,
            timestamp=received_timestamp_iso,
        )

        # Save the action to the database
        db.session.add(new_action)
        db.session.commit()

        return jsonify({"user_id": user_id, "action": action}), 200

    except Exception as e:
        # Log the exception
        logging.error(f"[Action] Error: {e}")
        return jsonify({"error": "Internal server error."}), 500
