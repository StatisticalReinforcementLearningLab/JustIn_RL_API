def test_add_user_success(test_client):
    """
    Tests adding a user successfully.
    """
    response = test_client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    assert response.status_code == 201
    assert response.json["user_id"] == "test_user_123"
    assert response.json["message"] == "User added successfully."


def test_add_user_duplicate(test_client):
    """
    Tests adding a duplicate user.
    """
    # Add the user for the first time
    test_client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    # Attempt to add the same user again
    response = test_client.post(
        "/api/v1/add_user",
        json={"user_id": "test_user_123"},
    )

    assert response.status_code == 400
    assert response.json["error"] == "User already exists."


def test_add_user_missing_field(test_client):
    """
    Tests adding a user without the required fields.
    """
    response = test_client.post(
        "/api/v1/add_user",
        json={},  # Missing `user_id`
    )

    assert response.status_code == 400
    assert response.json["error"] == "user_id is required."
