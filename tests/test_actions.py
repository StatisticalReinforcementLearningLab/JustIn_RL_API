def test_request_action_success(test_client):
    """
    Tests requesting an action for an existing user.
    """
    # Add a user
    test_client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    # Request an action
    response = test_client.post(
        "/api/v1/actions",
        json={
            "user_id": "test_user_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "context": {"example_key": "example_value"},
        },
    )

    assert response.status_code == 200
    assert response.json["user_id"] == "test_user_123"
    assert "action" in response.json


def test_request_action_user_not_found(test_client):
    """
    Tests requesting an action for a non-existent user.
    """
    response = test_client.post(
        "/api/v1/actions",
        json={
            "user_id": "non_existent_user",
            "timestamp": "2024-01-01T12:00:00Z",
            "context": {"example_key": "example_value"},
        },
    )

    assert response.status_code == 404
    assert response.json["error"] == "User not found."
