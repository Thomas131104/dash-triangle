import math

def test_gcg_valid(client):
    payload = {
        "angle_A": math.pi / 4,
        "edge": 6,
        "angle_B": math.pi / 6
    }

    response = client.post("/api/calculate/edge/gcg", json=payload)

    assert response.status_code == 200
    assert response.get_json()["success"] is True
