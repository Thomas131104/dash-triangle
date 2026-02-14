def test_ccc_valid(client):
    payload = {
        "edge_1": 3,
        "edge_2": 4,
        "edge_3": 5
    }

    response = client.post("/api/calculate/edge/ccc", json=payload)

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "area" in data["data"]
