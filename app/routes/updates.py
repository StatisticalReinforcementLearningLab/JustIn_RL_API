from flask import Blueprint, request, jsonify

updates_blueprint = Blueprint("updates", __name__)


@updates_blueprint.route("/update", methods=["POST"])
def update_model():
    """
    Updates the RL model with new data.
    """
    data = request.get_json()

    if not data or "update_data" not in data:
        return jsonify({"error": "update_data is required."}), 400

    update_data = data["update_data"]

    # Mock update logic
    print(f"Updating model with data: {update_data}")

    return jsonify({"message": "Model updated successfully."}), 200
