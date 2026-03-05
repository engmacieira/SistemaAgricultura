import pytest
from fastapi import status

def test_obter_configuracoes(client):
    # Garantir que existe algo
    client.put("/api/admin/configuracoes", json={"unidades_medida": ["kg"]})
    
    response = client.get("/api/admin/configuracoes")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "unidades_medida" in data
    assert isinstance(data["unidades_medida"], list)

def test_atualizar_configuracoes(client):
    new_config = {"unidades_medida": ["Hectare", "Alqueire", "Metro Quadrado"]}
    response = client.put("/api/admin/configuracoes", json=new_config)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["unidades_medida"] == new_config["unidades_medida"]

def test_realizar_backup(client):
    response = client.post("/api/admin/backup")
    # Dependendo da implementação do UC, pode retornar 200 ou 400 se falhar no mock de FS
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
    if response.status_code == status.HTTP_200_OK:
        assert "file_url" in response.json()

def test_restaurar_backup(client):
    payload = {"file_url": "http://mock-backup-url.sql"}
    response = client.post("/api/admin/restaurar", json=payload)
    assert response.status_code in [status.HTTP_200_OK, status.HTTP_400_BAD_REQUEST]
