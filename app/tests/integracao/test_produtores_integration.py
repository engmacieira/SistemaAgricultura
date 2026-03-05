import pytest
from fastapi import status

def test_criar_produtor(client):
    payload = {
        "name": "João da Silva",
        "cpfCnpj": "12345678901",
        "property": "Fazenda Sol Nascente",
        "regiao_referencia": "Comunidade A",
        "telefone_contato": "11999999999",
        "apelido_produtor": "Joao",
        "status": "Ativo"
    }
    response = client.post("/api/produtores/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
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
        "regiao_referencia": "Comunidade B",
        "telefone_contato": "11888888888",
        "apelido_produtor": "Maria",
        "status": "Ativo"
    }
    client.post("/api/produtores/", json=payload)
    
    response = client.get("/api/produtores/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "items" in data
    assert "total" in data
    assert isinstance(data["items"], list)
    assert len(data["items"]) >= 1

def test_obter_produtor(client):
    payload = {
        "name": "Carlos Santos",
        "cpfCnpj": "11122233344",
        "property": "Estância Gaúcha",
        "regiao_referencia": "Comunidade C",
        "telefone_contato": "11777777777",
        "apelido_produtor": "Carlos",
        "status": "Ativo"
    }
    create_res = client.post("/api/produtores/", json=payload)
    produtor_id = create_res.json()["id"]
    
    response = client.get(f"/api/produtores/{produtor_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == produtor_id
    assert data["name"] == payload["name"]

def test_atualizar_produtor(client):
    payload = {
        "name": "Pedro Rocha",
        "cpfCnpj": "55566677788",
        "property": "Fazenda Bela Vista",
        "regiao_referencia": "Comunidade D",
        "telefone_contato": "11666666666",
        "apelido_produtor": "Pedro",
        "status": "Ativo"
    }
    create_res = client.post("/api/produtores/", json=payload)
    produtor_id = create_res.json()["id"]
    
    update_payload = {"name": "Pedro Rocha Junior", "regiao_referencia": "Nova Região"}
    response = client.put(f"/api/produtores/{produtor_id}", json=update_payload)
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "Pedro Rocha Junior"
    assert data["regiao_referencia"] == "Nova Região"

def test_deletar_produtor(client):
    payload = {
        "name": "Deletar me",
        "cpfCnpj": "00000000000",
        "property": "Lote Vazio",
        "regiao_referencia": "Nenhuma",
        "telefone_contato": "Nenhum",
        "apelido_produtor": "Deletar",
        "status": "Inativo"
    }
    create_res = client.post("/api/produtores/", json=payload)
    produtor_id = create_res.json()["id"]
    
    response = client.delete(f"/api/produtores/{produtor_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT
    
    # Verificar se foi "deletado" (não aparece mais na listagem/obter)
    get_res = client.get(f"/api/produtores/{produtor_id}")
    assert get_res.status_code == status.HTTP_404_NOT_FOUND

def test_reativar_produtor_excluido(client):
    payload = {
        "name": "Maria Reativar",
        "cpfCnpj": "99999999991",
        "property": "Fazenda Teste",
        "regiao_referencia": "Região 1",
        "telefone_contato": "123",
        "apelido_produtor": "Maria",
        "status": "Ativo"
    }
    create_res = client.post("/api/produtores/", json=payload)
    produtor_id = create_res.json()["id"]
    
    # Deletar (Soft Delete)
    client.delete(f"/api/produtores/{produtor_id}")
    
    # Verificar que sumiu
    assert client.get(f"/api/produtores/{produtor_id}").status_code == 404
    
    # Tentar criar novamente com o mesmo CPF
    payload["name"] = "Maria Reativada"
    response = client.post("/api/produtores/", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] == produtor_id # Deve ser o mesmo ID
    assert data["name"] == "Maria Reativada"
    assert data["is_deleted"] == False

def test_erro_cpf_duplicado_ativo(client):
    payload = {
        "name": "Joao Duplicado",
        "cpfCnpj": "88888888888",
        "property": "Fazenda Teste",
        "regiao_referencia": "Região 1",
        "telefone_contato": "123",
        "apelido_produtor": "Joao",
        "status": "Ativo"
    }
    client.post("/api/produtores/", json=payload)
    
    # Tentar criar novamente
    response = client.post("/api/produtores/", json=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "já está cadastrado" in response.json()["detail"]
