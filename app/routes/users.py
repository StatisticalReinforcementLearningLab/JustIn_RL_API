from flask import Blueprint, request, jsonify
from app.models import User
from app.extensions import db

users_blueprint = Blueprint("users", __name__)

@users_blueprint.route("/add_user", methods=["POST"])
def add_user():
    """
    Adds a new user to the database.
    """
    data = request.get_json()

    if not data or "user_id" not in data:
        return jsonify({"error": "user_id is required."}), 400

    user_id = data["user_id"]

    # Check if the user already exists
    existing_user = User.query.filter_by(user_id=user_id).first()
    if existing_user:
        return jsonify({"error": "User already exists."}), 400

    # Add new user
    new_user = User(user_id=user_id)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"user_id": user_id, "message": "User added successfully."}), 201
