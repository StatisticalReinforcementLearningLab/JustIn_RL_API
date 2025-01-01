import datetime
import logging
import uuid
import requests
from threading import Thread
from flask import Blueprint, current_app, request, jsonify
from app.models import ModelParameters, StudyData, ModelUpdateRequests
from app.algorithms.base import RLAlgorithm
from app.extensions import db

update_blueprint = Blueprint("update", __name__)


def process_update_request(
    app, update_id: str, rl_algorithm: RLAlgorithm, callback_url: str
):
    """
    Process the update request.
    """
    try:
        with app.app_context():
            # Get the latest model parameters from the database
            current_params = ModelParameters.query.order_by(
                ModelParameters.timestamp.desc()
            ).first()

            # Get the data required for the update
            # In this case, it is all the temperatures and the
            # reward values from the study data
            study_data = StudyData.query.all()
            temperatures = [data.raw_context["temperature"] for data in study_data]
            rewards = [data.reward for data in study_data]

            # Update the model parameters
            status, new_parameters = rl_algorithm.update(
                {"probability_of_action": current_params.probability_of_action},
                {"temperatures": temperatures, "rewards": rewards},
            )

            if not status:
                raise Exception("Model update failed.")

            # Add the new model parameters to the database
            new_model_parameters = ModelParameters(new_parameters["probability_of_action"])

            db.session.add(new_model_parameters)
            db.session.commit()

            # Update the status of the request
            model_update_request = ModelUpdateRequests.query.filter_by(
                update_id=update_id
            ).first()
            model_update_request.status = "completed"
            model_update_request.completed_at = datetime.datetime.now().isoformat()
            db.session.commit()

            # Send a callback to the callback URL
            requests.post(callback_url, json={"status": "completed", "timestamp": datetime.datetime.now().isoformat()})

            # Log the completion
            logging.info(f"[Update] Update ID: {update_id} completed.")

    except Exception as e:
        with app.app_context():
            # Log the error
            logging.error(f"[Update] Error: {e}")

            # Update the status of the request
            model_update_request = ModelUpdateRequests.query.filter_by(
                update_id=update_id
            ).first()
            model_update_request.status = "failed"
            model_update_request.completed_at = datetime.datetime.now().isoformat()
            model_update_request.error_message = str(e)
            db.session.commit()

            # Send a callback to the callback URL
            requests.post(
                callback_url, json={"status": "failed", "message": "Model update failed."}
            )

            # Log the completion
            logging.info(f"[Update] Update ID: {update_id} failed.")


def check_fields(data: dict) -> tuple[bool, str]:
    """
    Check if the required fields are present in the data.
    """
    if not data or "timestamp" not in data:
        return False, "timestamp is required."

    if "callback_url" not in data:
        return False, "callback_url is required."

    return True, ""


@update_blueprint.route("/update", methods=["POST"])
def update_model():
    """
    Updates the algorithm model.
    """
    try:
        data = request.get_json()

        # Check if the required fields are present
        fields_present, error_message = check_fields(data)
        if not fields_present:
            return jsonify({"status": "failed", "message": error_message}), 400

        # Extract the data
        request_timestamp = data["timestamp"]
        callback_url = data["callback_url"]

        # Get the RL algorithm
        rl_algorithm = current_app.rl_algorithm

        # Generate a unique update ID for the request
        update_id = str(uuid.uuid4())
        logging.info(f"[Update] Update ID: {update_id}")

        # Add the update request to the database
        model_update_request = ModelUpdateRequests(
            update_id, callback_url, request_timestamp
        )
        db.session.add(model_update_request)
        db.session.commit()

        # Process the update request in a separate thread
        app = current_app._get_current_object()  # Get the actual app object
        thread = Thread(
            target=process_update_request,
            args=(app, update_id, rl_algorithm, callback_url),
        )
        thread.start()

        return jsonify({"status": "processing", "update_id": update_id}), 202

    except Exception as e:
        # Log the error
        logging.error(f"[Update] Error: {e}")
        logging.exception(e)
        return jsonify({"error": "Internal server error."}), 500
