import logging
from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db

user_blueprint = Blueprint("user", __name__)

def check_fields(data: dict) -> tuple[bool, str]:
    """
    Check if the required fields are present in the data.
    """
    if not data or "user_id" not in data:
        return False, "user_id is required."

    return True, ""

@user_blueprint.route("/add_user", methods=["POST"])
def add_user():
    """
    Adds a new user to the database.
    """
    try:
        data = request.get_json()

        # Check if the required fields are present
        fields_present, error_message = check_fields(data)
        if not fields_present:
            return jsonify({"error": error_message}), 400

        # Extract the data
        user_id = data["user_id"]

        # Check if the user already exists
        existing_user = User.query.filter_by(user_id=user_id).first()
        if existing_user:
            return jsonify({"error": "User already exists."}), 400

        # Add new user
        new_user = User(user_id=user_id)
        db.session.add(new_user)
        db.session.commit()

        # Log the user addition
        logging.info(f"[User] User added: {user_id}")

        return jsonify({"user_id": user_id, "message": "User added successfully."}), 201

    except Exception as e:
        logging.error(f"[User] Error: {e}")
        return jsonify({"error": "Internal server error."}), 500