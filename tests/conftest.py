import pytest
from fastapi.testclient import TestClient
from mock_server.mock_app import app, fake_users_db

@pytest.fixture(scope="session")
def client():
    """Współdzielona instancja klienta testowego dla całej sesji."""
    return TestClient(app)

@pytest.fixture(autouse=True)
def reset_database():
    """
    Izolacja stanu: baza jest czyszczona i seedowana przed KAŻDYM testem.
    Dzięki temu kolejność wykonywania testów nie ma znaczenia.
    """
    fake_users_db.clear()
    fake_users_db[1] = {
        "id": 1, 
        "name": "Anna Kowalska", 
        "email": "anna@test.pl", 
        "role": "admin"
    }
    yield
    fake_users_db.clear()