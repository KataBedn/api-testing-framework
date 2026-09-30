import pytest

@pytest.mark.parametrize("invalid_email", [
    "invalid-email",
    "plainaddress",
    "@missingusername.com",
    "missing_domain@.com"
])
def test_create_user_with_invalid_email_returns_422(client, invalid_email):
    """Walidacja formatu e-maila wymuszana przez pydantic[email]."""
    payload = {
        "name": "Jan Tester",
        "email": invalid_email,
        "role": "tester"
    }
    response = client.post("/users", json=payload)
    assert response.status_code == 422
    
    errors = response.json().get("detail", [])
    assert any(err["loc"][-1] == "email" for err in errors)

@pytest.mark.parametrize("missing_field", ["name", "email"])
def test_create_user_missing_required_fields_returns_422(client, missing_field):
    """Walidacja wymaganych pól w payloadzie JSON."""
    payload = {
        "name": "Jan Tester",
        "email": "jan@tester.com"
    }
    del payload[missing_field]

    response = client.post("/users", json=payload)
    assert response.status_code == 422