def test_get_user_success(client):
    response = client.get("/users/1")
    assert response.status_code == 200
    
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Anna Kowalska"

def test_get_user_not_found(client):
    response = client.get("/users/999")
    assert response.status_code == 404
    assert "not exist" in response.json()["detail"].lower()

def test_create_user_success(client):
    new_user = {
        "name": "Piotr QA",
        "email": "piotr.qa@company.com",
        "role": "automation"
    }
    response = client.post("/users", json=new_user)
    assert response.status_code == 201
    
    created_data = response.json()
    assert created_data["id"] == 2
    assert created_data["email"] == "piotr.qa@company.com"

    # Weryfikacja persystencji stanu:
    verify_response = client.get(f"/users/{created_data['id']}")
    assert verify_response.status_code == 200

def test_delete_user_success(client):
    # Usunięcie rekordu
    delete_res = client.delete("/users/1")
    assert delete_res.status_code == 204

    # Weryfikacja usunięcia
    get_res = client.get("/users/1")
    assert get_res.status_code == 404