import datetime
import logging
import uuid
from threading import Thread
from flask import Blueprint, current_app, request, jsonify
from app.models import ModelParameters, StudyData, ModelUpdateRequests
from app.extensions import db

update_blueprint = Blueprint("update", __name__)

def process_update_request(update_id: str, rl_algorithm, callback_url: str):
    """
    Process the update request.
    """
    try:
        # Get the latest model parameters from the database
        model_parameters = ModelParameters.query.order_by(
            ModelParameters.created_at.desc()
        ).first()

        # Get the data required for the update
        # In this case, it is all the temperature data in the study_data table
        study_data = StudyData.query.all()
        temperatures = [data.temperature for data in study_data]

        # Update the model parameters
        rl_algorithm.update_model(temperatures)


        # Get the probability of action
        probability_of_action = model_parameters.probability_of_action

        # Update the model
        rl_algorithm.update_model(probability_of_action)

        # Update the status of the request
        model_update_request = ModelUpdateRequests.query.filter_by(update_id=update_id).first()
        model_update_request.status = "completed"
        model_update_request.completed_at = datetime.datetime.now().isoformat()
        db.session.commit()

        # Log the completion
        logging.info(f"[Update] Update ID: {update_id} completed.")

    except Exception as e:
        # Log the error
        logging.error(f"[Update] Error: {e}")

        # Update the status of the request
        model_update_request = ModelUpdateRequests.query.filter_by(update_id=update_id).first()
        model_update_request.status = "failed"
        model_update_request.completed_at = datetime.datetime.now().isoformat()
        model_update_request.error_message = str(e)
        db.session.commit()

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
            return jsonify({"error": error_message}), 400
        
        # Extract the data
        request_timestamp = data["timestamp"]
        callback_url = data["callback_url"]
        received_timestamp_iso = datetime.datetime.now().isoformat()

        # Get the RL algorithm
        rl_algorithm = current_app.rl_algorithm

        # Generate a unique update ID for the request
        update_id = str(uuid.uuid4())
        logging.info(f"[Update] Update ID: {update_id}")

        # Add the update request to the database
        model_update_request = ModelUpdateRequests(update_id, callback_url)
        db.session.add(model_update_request)
        db.session.commit()

        # Process the update request in a separate thread
        thread = Thread(
            target=process_update_request,
            args=(update_id, rl_algorithm, callback_url),
        )
        thread.start()

        return jsonify({"update_id": update_id, "status": "processing"}), 202

    except Exception as e:
        # Log the error
        logging.error(f"[Update] Error: {e}")
        return jsonify({"error": "Internal server error."}), 500