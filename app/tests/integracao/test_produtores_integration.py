import pytest
from fastapi import status

def test_criar_produtor(client):
    payload = {
        "name": "João da Silva",
        "cpfCnpj": "12345678901",
        "property": "Fazenda Sol Nascente",
        "totalArea": 150.5,
        "status": "Ativo"
    }
    response = client.post("/produtores/", json=payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == payload["name"]
    assert data["cpfCnpj"] == payload["cpfCnpj"]
    assert "id" in data

def test_listar_produtores(client):
    # Criar um produtor primeiro
    payload = {
        "name": "Maria Oliveira",
        "cpfCnpj": "98765432100",
        "property": "Sítio Primavera",
        "totalArea": 80.0,
        "status": "Ativo"
    }
    client.post("/produtores/", json=payload)
    
    response = client.get("/produtores/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1

def test_obter_produtor(client):
    payload = {
        "name": "Carlos Santos",
        "cpfCnpj": "11122233344",
        "property": "Estância Gaúcha",
        "totalArea": 300.0,
        "status": "Ativo"
    }
    create_res = client.post("/produtores/", json=payload)
    produtor_id = create_res.json()["id"]
    
    response = client.get(f"/produtores/{produtor_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == produtor_id
    assert data["name"] == payload["name"]

def test_atualizar_produtor(client):
    payload = {
        "name": "Pedro Rocha",
        "cpfCnpj": "55566677788",
        "property": "Fazenda Bela Vista",
        "totalArea": 200.0,
        "status": "Ativo"
    }
    create_res = client.post("/produtores/", json=payload)
    produtor_id = create_res.json()["id"]
    
    update_payload = {"name": "Pedro Rocha Junior", "totalArea": 210.0}
    response = client.put(f"/produtores/{produtor_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Pedro Rocha Junior"
    assert data["totalArea"] == 210.0

def test_deletar_produtor(client):
    payload = {
        "name": "Deletar me",
        "cpfCnpj": "00000000000",
        "property": "Lote Vazio",
        "totalArea": 10.0,
        "status": "Inativo"
    }
    create_res = client.post("/produtores/", json=payload)
    produtor_id = create_res.json()["id"]
    
    response = client.delete(f"/produtores/{produtor_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Produtor deletado com sucesso"
    
    # Verificar se foi deletado
    get_res = client.get(f"/produtores/{produtor_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND
