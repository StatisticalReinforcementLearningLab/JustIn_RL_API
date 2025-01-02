import pytest
import uuid
import requests
from flask import Flask, request, jsonify
from threading import Thread
from app.models import ModelUpdateRequests, db
from flask import current_app
import time

# Mock Flask Callback Server
mock_app = Flask(__name__)
callback_responses = []  # Store callback responses for verification


@mock_app.route("/callback", methods=["POST"])
def callback():
    """
    Mock callback endpoint to capture callback data.
    """
    data = request.get_json()
    callback_responses.append(data)  # Store the received data for verification
    return jsonify({"message": "Callback received"}), 200

def run_mock_server():
    """
    Runs the mock callback server.
    """
    mock_app.run(port=5001, use_reloader=False)

@pytest.fixture(scope="module", autouse=True)
def start_mock_server():
    """
    Starts the mock callback server in a separate thread.
    """
    server_thread = Thread(target=run_mock_server)
    server_thread.daemon = True
    server_thread.start()
    time.sleep(1)  # Allow the server to start
    yield
    # No explicit teardown needed since the thread is daemonized

def test_update_model_success(client):
    """
    Tests updating the model successfully.
    """

    # Add user
    response = client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    # Now request an action
    response = client.post(
        "/api/v1/action",
        json={
            "user_id": "test_user_123",
            "timestamp": "2025-01-01T12:00:00",
            "decision_idx": 0,
            "context": {"temperature": 25.0},
        },
    )

    assert response.status_code == 201

    # Now use the action and report it back as data with some outcome

    response = client.post(
        "/api/v1/upload_data",
        json={
            "user_id": "test_user_123",
            "timestamp": "2025-01-01T12:00:00",
            "decision_idx": 0,
            "data": {
                "context": {"temperature": 25.0},
                "action": response.json["action"],
                "action_prob": response.json["action_prob"],
                "state": response.json["state"],
                "outcome": {"clicks": 4},
            },
        },
    )

    assert response.status_code == 201

    # Now update the model

    callback_url = "http://127.0.0.1:5001/callback"

    response = client.post(
        "/api/v1/update",
        json={
            "callback_url": callback_url,
            "timestamp": "2025-01-01T12:00:00",
        },
    )

    assert response.status_code == 202
    assert response.json["status"] == "processing"
    data = response.get_json()
    assert "update_id" in data
    update_id = data["update_id"]

    # Sleep for a while to allow the model update to complete
    time.sleep(7)

    # Verify the callback response
    assert len(callback_responses) == 1
    callback_data = callback_responses[0]
    print(callback_data)
    assert callback_data["update_id"] == update_id
    assert callback_data["status"] == "completed"
