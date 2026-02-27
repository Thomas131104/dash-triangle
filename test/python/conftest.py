import pytest
from server import server


@pytest.fixture
def client():
    server.config["TESTING"] = True

    with server.test_client() as client:
        yield client
