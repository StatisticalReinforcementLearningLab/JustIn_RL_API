import logging
import datetime
from flask import Blueprint, request, jsonify, current_app
from app.extensions import db
from app.models import User, Action, ModelParameters, StudyData

action_blueprint = Blueprint("action", __name__)


def check_fields(data: dict) -> tuple[bool, str]:
    """
    Check if the required fields are present in the data.
    """
    if not data or "user_id" not in data or "timestamp" not in data:
        return False, "user_id and timestamp are required."

    if "decision_idx" not in data:
        return False, "decision_idx is required."

    if "context" not in data:
        return False, "context is required."

    if "temperature" not in data["context"]:
        return False, "Invalid context. Temperature is required."

    # Check field types
    if not isinstance(data["user_id"], str):
        return False, "user_id must be a string."

    if not isinstance(data["timestamp"], str) and not isinstance(
        data["timestamp"], datetime.datetime
    ):
        return False, "timestamp must be a string or datetime object."

    if not isinstance(data["decision_idx"], int):
        return False, "decision_idx must be an integer."

    if not isinstance(data["context"], dict):
        return False, "context must be a dictionary."

    if not isinstance(data["context"]["temperature"], float) and not isinstance(
        data["context"]["temperature"], int
    ):
        return False, "temperature must be a float or int."

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
            return jsonify({"status": "failed", "message": error_message}), 400

        # Extract the data
        user_id = data["user_id"]
        decision_idx = data["decision_idx"]
        context = data["context"]
        request_timestamp = data["timestamp"]
        received_timestamp_iso = datetime.datetime.now().isoformat()

        # Check if the user exists in the database
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"status": "failed", "message": "User not found."}), 404

        # Check if decision_idx does not exist in the study data for the user
        study_data = StudyData.query.filter_by(
            user_id=user_id, decision_idx=decision_idx
        ).first()
        if study_data:
            return (
                jsonify(
                    {"status": "failed", "message": "Decision index already exists."}
                ),
                400,
            )

        # Get the RL algorithm
        rl_algorithm = current_app.rl_algorithm

        # Make the state
        status, state = rl_algorithm.make_state(context)
        if not status:
            return jsonify({"status": "failed", "message": state}), 400

        # Get the latest model parameters from the database
        model_parameters = ModelParameters.query.order_by(
            ModelParameters.timestamp.desc()
        ).first()

        # Check if the model parameters exist
        if not model_parameters:
            return (
                jsonify({"status": "failed", "message": "Model parameters not found."}),
                404,
            )

        # Extract the model parameters, in this case, the probability
        probability = model_parameters.probability_of_action

        # Get the action, action selection probability, and random state
        # used to generate the action
        action, prob, random_state = rl_algorithm.get_action(
            user_id, state, {"probability": probability}, decision_idx
        )

        # Save the action to the action database
        new_action = Action(
            user_id=user_id,
            action=action,
            state=state,
            decision_idx=decision_idx,
            raw_context=context,
            action_prob=prob,
            random_state=random_state,
            model_parameters_id=model_parameters.id,
            request_timestamp=request_timestamp,
            timestamp=received_timestamp_iso,
        )

        # Save the action to the database
        db.session.add(new_action)
        db.session.commit()

        return (
            jsonify(
                {
                    "status": "success",
                    "user_id": user_id,
                    "state": state,
                    "action": action,
                    "action_prob": prob,
                    "timestamp": received_timestamp_iso,
                }
            ),
            201,
        )

    except Exception as e:
        # Log the exception
        logging.error(f"[Action] Error: {e}")
        logging.exception(e)
        return jsonify({"status": "failed", "message": "Internal server error."}), 500
