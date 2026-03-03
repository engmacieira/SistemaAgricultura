import pytest
from fastapi import status

def test_criar_usuario(client):
    payload = {
        "name": "Admin Teste",
        "email": "admin@teste.com",
        "role": "admin",
        "password": "senha123"
    }
    response = client.post("/usuarios/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
    assert "password" not in data # Segurança: não deve retornar senha

def test_login_usuario(client):
    # 1. Criar usuário
    payload = {
        "name": "User Login",
        "email": "login@teste.com",
        "role": "user",
        "password": "password123"
    }
    client.post("/usuarios/", json=payload)
    
    # 2. Tentar login
    login_payload = {
        "email": "login@teste.com",
        "password": "password123"
    }
    response = client.post("/usuarios/login", json=login_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "login@teste.com"
    # assert "token" in data # Se houver JWT implementado no UC

def test_login_falha(client):
    login_payload = {
        "email": "inexistente@teste.com",
        "password": "errada"
    }
    response = client.post("/usuarios/login", json=login_payload)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

def test_alterar_senha(client):
    # 1. Criar
    payload = {
        "name": "User Senha",
        "email": "senha@teste.com",
        "role": "user",
        "password": "velha"
    }
    create_res = client.post("/usuarios/", json=payload)
    user_id = create_res.json()["id"]
    
    # 2. Alterar
    alterar_payload = {
        "senha_atual": "velha",
        "nova_senha": "nova"
    }
    response = client.put(f"/usuarios/{user_id}/senha", json=alterar_payload)
    assert response.status_code == status.HTTP_200_OK
    
    # 3. Validar login com nova senha
    login_payload = {
        "email": "senha@teste.com",
        "password": "nova"
    }
    login_res = client.post("/usuarios/login", json=login_payload)
    assert login_res.status_code == status.HTTP_200_OK
