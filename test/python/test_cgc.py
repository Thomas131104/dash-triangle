import math

def test_cgc_valid(client):
    payload = {
        "edge_1": 5,
        "edge_2": 7,
        "angle_C": math.pi / 3
    }

    response = client.post("/api/calculate/edge/cgc", json=payload)

    assert response.status_code == 200
    assert response.get_json()["success"] is True
