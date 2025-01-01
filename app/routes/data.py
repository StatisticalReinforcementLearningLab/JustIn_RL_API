import datetime
import logging
import uuid
import requests
from threading import Thread
from flask import Blueprint, current_app, request, jsonify
from app.models import User, ModelParameters, StudyData, ModelUpdateRequests
from app.algorithms.base import RLAlgorithm
from app.extensions import db

data_blueprint = Blueprint("data", __name__)


def check_fields(data: dict) -> tuple[bool, str]:
    """
    Check if the required fields are present in the data.
    """
    if not data or "user_id" not in data:
        return False, "user_id is required."

    if "decision_idx" not in data:
        return False, "decision_idx is required."

    if "timestamp" not in data:
        return False, "timestamp is required."

    if "data" not in data:
        return False, "data is required."

    user_data = data["data"]

    if not user_data or "context" not in user_data:
        return False, "context is required."

    if "temperature" not in user_data["context"]:
        return False, "Invalid context. Temperature is required."

    if "action" not in user_data:
        return False, "action is required."

    if "action_prob" not in user_data:
        return False, "action_prob is required."
    
    if "state" not in user_data:
        return False, "state is required."

    if "outcome" not in user_data:
        return False, "outcome is required."

    if "clicks" not in user_data["outcome"]:
        return False, "Invalid outcome. Clicks is required."

    return True, ""


@data_blueprint.route("/upload_data", methods=["POST"])
def upload_data():
    """
    Uploads interaction data for a specific user, along with
    the action sent and the timestamp (and associated metadata).
    """
    try:
        data = request.get_json()

        # Check if the required fields are present
        fields_present, error_message = check_fields(data)
        if not fields_present:
            return jsonify({"status": "failed", "message": error_message}), 400

        # Extract the user_id
        user_id = data["user_id"]

        # Check if the user exists
        user = User.query.filter_by(user_id=user_id).first()
        if not user:
            return jsonify({"status": "failed", "message": "User not found."}), 404

        # Extract the decision index
        decision_idx = data["decision_idx"]

        # Check if the decision index already exists
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

        # Extract the rest of the data
        request_timestamp = data["timestamp"]
        user_data = data["data"]
        context = user_data["context"]
        action = user_data["action"]
        action_prob = user_data["action_prob"]
        state = user_data["state"]
        outcome = user_data["outcome"]

        # Get the RL algorithm
        rl_algorithm = current_app.rl_algorithm

        # Create the reward based on the outcome
        status, reward = rl_algorithm.make_reward(user_id, state, action, outcome)

        if not status:
            return jsonify({"status": "failed", "message": "Reward creation failed."}), 400

        # Save the data to the database
        study_data = StudyData(
            user_id=user_id,
            decision_idx=decision_idx,
            action=action,
            action_prob=action_prob,
            state=state,
            raw_context=context,
            outcome=outcome,
            reward=reward,
            request_timestamp=request_timestamp,
        )
        db.session.add(study_data)
        db.session.commit()

        # Log the completion
        logging.info(f"[Upload Data] Data uploaded for user: {user_id}")

        return jsonify({"status": "success", "message": "Data uploaded successfully."}), 201

    except Exception as e:
        # Log the error
        logging.error(f"[Upload Data] Error: {e}")
        logging.exception(e)
        return jsonify({"error": "Internal Server Error"}), 500
