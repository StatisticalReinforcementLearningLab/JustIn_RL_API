import pytest
from app.routes.action import check_fields, request_action
from app.models import User, StudyData
from unittest.mock import patch, MagicMock

# Test check_fields for all scenarios
def test_check_fields_missing_user_id():
    data = {"timestamp": "2025-01-01T12:00:00", "decision_idx": 0, "context": {"temperature": 22}}
    result, error_message = check_fields(data)
    assert not result
    assert "user_id and timestamp are required." in error_message

def test_check_fields_missing_timestamp():
    data = {"user_id": "test_user_123", "decision_idx": 0, "context": {"temperature": 22}}
    result, error_message = check_fields(data)
    assert not result
    assert "user_id and timestamp are required." in error_message

def test_check_fields_missing_decision_idx():
    data = {"user_id": "test_user_123", "timestamp": "2025-01-01T12:00:00", "context": {"temperature": 22}}
    result, error_message = check_fields(data)
    assert not result
    assert "decision_idx is required." in error_message

def test_check_fields_missing_context():
    data = {"user_id": "test_user_123", "timestamp": "2025-01-01T12:00:00", "decision_idx": 0}
    result, error_message = check_fields(data)
    assert not result
    assert "context is required." in error_message

def test_check_fields_missing_temperature():
    data = {"user_id": "test_user_123", "timestamp": "2025-01-01T12:00:00", "decision_idx": 0, "context": {}}
    result, error_message = check_fields(data)
    assert not result
    assert "Invalid context. Temperature is required." in error_message

# Now all the fields with wrong data types
def test_check_fields_user_id_not_string():
    data = {"user_id": 123, "timestamp": "2025-01-01T12:00:00", "decision_idx": 0, "context": {"temperature": 22}}
    result, error_message = check_fields(data)
    assert not result
    assert "user_id must be a string." in error_message

def test_check_fields_timestamp_not_string():
    data = {"user_id": "test_user_123", "timestamp": 123, "decision_idx": 0, "context": {"temperature": 22}}
    result, error_message = check_fields(data)
    assert not result
    assert "timestamp must be a string or datetime object." in error_message

def test_check_fields_decision_idx_not_int():
    data = {"user_id": "test_user_123", "timestamp": "2025-01-01T12:00:00", "decision_idx": "0", "context": {"temperature": 22}}
    result, error_message = check_fields(data)
    assert not result
    assert "decision_idx must be an integer." in error_message

def test_check_fields_context_not_dict():
    data = {"user_id": "test_user_123", "timestamp": "2025-01-01T12:00:00", "decision_idx": 0, "context": "temperature"}
    result, error_message = check_fields(data)
    assert not result
    assert "context must be a dictionary." in error_message

def test_check_fields_temperature_not_float_or_int():
    data = {"user_id": "test_user_123", "timestamp": "2025-01-01T12:00:00", "decision_idx": 0, "context": {"temperature": "22"}}
    result, error_message = check_fields(data)
    assert not result
    assert "temperature must be a float or int." in error_message

# Finally, a valid data

def test_check_fields_valid():
    data = {"user_id": "test_user_123", "timestamp": "2025-01-01T12:00:00", "decision_idx": 0, "context": {"temperature": 22}}
    result, error_message = check_fields(data)
    assert result
    assert error_message == ""

# Test request_action for all scenarios
# Test request_action_missing_user
@patch("app.routes.action.User.query")
def test_request_action_missing_user(mock_user_query, client):
    mock_user_query.filter_by.return_value.first.return_value = None
    response = client.post("/api/v1/action", json={
        "user_id": "test_user_123",
        "timestamp": "2025-01-01T12:00:00",
        "decision_idx": 0,
        "context": {"temperature": 22}
    })
    assert response.status_code == 404
    assert response.json["message"] == "User not found."

# Test request_action_success
def test_request_action_success(client):
    with patch("app.routes.action.User.query") as mock_user_query, \
         patch("app.routes.action.StudyData.query") as mock_study_data_query:
        mock_user_query.filter_by.return_value.first.return_value = MagicMock()
        mock_study_data_query.filter_by.return_value.first.return_value = None

        response = client.post("/api/v1/action", json={
            "user_id": "test_user_123",
            "timestamp": "2025-01-01T12:00:00",
            "decision_idx": 0,
            "context": {"temperature": 22}
        })
        assert response.status_code == 201
        assert response.json["status"] == "success"