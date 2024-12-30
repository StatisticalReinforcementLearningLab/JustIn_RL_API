def test_update_model_success(test_client):
    """
    Tests updating the model successfully.
    """
    response = test_client.post(
        "/api/v1/update",
        json={"update_data": {"key": "value"}},
    )

    assert response.status_code == 200
    assert response.json["message"] == "Model updated successfully."


def test_update_model_missing_field(test_client):
    """
    Tests updating the model without required fields.
    """
    response = test_client.post(
        "/api/v1/update",
        json={},  # Missing `update_data`
    )

    assert response.status_code == 400
    assert response.json["error"] == "update_data is required."
