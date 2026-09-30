from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Dict, Optional

app = FastAPI(title="Local QA Mock Server")

# 1. Model danych przyjmowany w POST (klient nie wysyła ID, ID nadaje serwer)
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    role: str = "tester"

# 2. Model danych zwracany przez API (z wygenerowanym ID)
class UserResponse(UserCreate):
    id: int

# In-memory "baza danych" do testów (słownik w pamięci)
fake_users_db: Dict[int, dict] = {
    1: {"id": 1, "name": "Anna Kowalska", "email": "anna@test.pl", "role": "admin"}
}

# --- ENDPOINTY ---

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    """Zwraca usera lub 404, jeśli brak w bazie."""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail=f"User with ID {user_id} does not exist"
        )
    return fake_users_db[user_id]


@app.post("/users", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate):
    """Tworzy nowego usera i zapisuje w fake_users_db."""
    # Generowanie prostego auto-increment ID
    new_id = max(fake_users_db.keys(), default=0) + 1
    
    user_data = user.model_dump()
    user_data["id"] = new_id
    
    fake_users_db[new_id] = user_data
    return user_data


@app.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    """Usuwa usera lub zwraca 404."""
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
    del fake_users_db[user_id]
    return None