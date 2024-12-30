def test_upload_data_success(test_client):
    """
    Tests uploading interaction data successfully.
    """
    # Add a user
    test_client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    # Upload data
    response = test_client.post(
        "/api/v1/upload_data",
        json={
            "user_id": "test_user_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "data": {"key": "value", "interaction": "click"},
        },
    )

    assert response.status_code == 200
    assert response.json["message"] == "Data uploaded successfully."


def test_upload_data_user_not_found(test_client):
    """
    Tests uploading data for a non-existent user.
    """
    response = test_client.post(
        "/api/v1/upload_data",
        json={
            "user_id": "non_existent_user",
            "timestamp": "2024-01-01T12:00:00Z",
            "data": {"key": "value", "interaction": "click"},
        },
    )

    assert response.status_code == 404
    assert response.json["error"] == "User not found."
