import pytest
from app.routes.user import check_fields, add_user
from app.models import User, StudyData
from unittest.mock import patch, MagicMock

# Test check_fields for user route
def test_check_fields_user_missing_username():
    data = {}
    result, error_message = check_fields(data)
    assert not result
    assert "user_id is required." in error_message

def test_check_fields_user_valid():
    data = {"user_id": "test_user_123"}
    result, error_message = check_fields(data)
    assert result
    assert error_message == ""

def test_add_user_missing_field(client):
    """
    Tests adding a user without the required fields.
    """
    response = client.post(
        "/api/v1/add_user",
        json={},  # Missing `user_id`
    )

    assert response.status_code == 400
    assert response.json["message"] == "user_id is required."



def test_add_user_duplicate(client):
    """
    Tests adding a duplicate user.
    """
    # Add the user for the first time
    client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    # Attempt to add the same user again
    response = client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    assert response.status_code == 400
    assert response.json["message"] == "User already exists."


def test_add_user_success(client):
    """
    Tests adding a user successfully.
    """

    response = client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    print(response.json)

    assert response.status_code == 201
    assert response.json["user_id"] == "test_user_123"
    assert response.json["message"] == "User added successfully."
