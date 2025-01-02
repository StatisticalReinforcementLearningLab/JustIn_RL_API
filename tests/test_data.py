def test_upload_data_success(client):
    """
    Tests uploading interaction data successfully.
    """
    # Add a user
    client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    # Upload data
    response = client.post(
        "/api/v1/upload_data",
        json={
            "user_id": "test_user_123",
            "timestamp": "2024-01-01T12:00:00Z",
            "decision_idx": 0,
            "data": {
                "context": {"temperature": 23},
                "action": 1,
                "action_prob": 0.5,
                "state": [23],
                "outcome": {"clicks": 4},
            },
        },
    )

    print(response.json)

    assert response.status_code == 201
    assert response.json["message"] == "Data uploaded successfully."


def test_upload_data_user_not_found(client):
    """
    Tests uploading data for a non-existent user.
    """
    response = client.post(
        "/api/v1/upload_data",
        json={
            "user_id": "non_existent_user",
            "timestamp": "2024-01-01T12:00:00Z",
            "decision_idx": 2,
            "data": {
                "context": {"temperature": 30},
                "action": 1,
                "action_prob": 0.5,
                "state": [30],
                "outcome": {"clicks": 4},
            },
        },
    )
    print(response.json)

    assert response.status_code == 404
    assert response.json["message"] == "User not found."
