def test_coords_valid(client):
    payload = {
        "x1": 0,
        "y1": 0,
        "x2": 4,
        "y2": 0,
        "x3": 1,
        "y3": 3
    }

    response = client.post("/api/calculate/coords", json=payload)

    assert response.status_code == 200

    data = response.get_json()

    assert data["success"] is True
    assert "area" in data["data"]
