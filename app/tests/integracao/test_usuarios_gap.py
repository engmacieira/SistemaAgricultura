import pytest
from fastapi import status

def test_listar_usuarios_paginacao_ordenacao(client):
    # Setup: Ensure there are enough users (already some from other tests potentially, 
    # but we depend on the isolated session)
    # The current user 'Admin Test' already exists.
    
    response = client.get("/api/usuarios/?limit=5&sort_by=name&order=asc")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert len(data["items"]) <= 5

def test_soft_delete_usuario(client):
    # Setup: Create a user
    payload = {
        "name": "User Deletar",
        "email": "del@teste.com",
        "password": "password123",
        "role": "operador"
    }
    create_res = client.post("/api/usuarios/", json=payload)
    user_id = create_res.json()["id"]
    
    # Delete (Soft Delete)
    del_res = client.delete(f"/api/usuarios/{user_id}")
    assert del_res.status_code == status.HTTP_204_NO_CONTENT
    
    # Verify it doesn't appear in normal list
    list_res = client.get("/api/usuarios/")
    users = list_res.json()["items"]
    assert not any(u["id"] == user_id for u in users)
    
    # Verify it can't be retrieved via GET
    get_res = client.get(f"/api/usuarios/{user_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
