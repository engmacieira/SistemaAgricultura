from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_get_dashboard_data():
    """
    Testa se o endpoint do dashboard retorna a estrutura correta de dados.
    """
    response = client.get("/dashboard/")
    assert response.status_code == 200
    
    data = response.json()
    
    # Verifica estrutura do summary
    assert "summary" in data
    assert "totalProducers" in data["summary"]
    assert "totalServices" in data["summary"]
    assert "pendingExecutions" in data["summary"]
    assert "totalPendingAmount" in data["summary"]
    assert "totalPaidAmount" in data["summary"]
    
    # Verifica estrutura dos outros campos
    assert "monthlyFinancial" in data
    assert "serviceDistribution" in data
    assert "recentActivities" in data
    
    # Verifica se os campos são listas
    assert isinstance(data["monthlyFinancial"], list)
    assert isinstance(data["serviceDistribution"], list)
    assert isinstance(data["recentActivities"], list)

def test_dashboard_data_integrity():
    """
    Testa a integridade mínima dos dados retornados.
    """
    response = client.get("/dashboard/")
    data = response.json()
    
    # Valores não devem ser negativos
    assert data["summary"]["totalProducers"] >= 0
    assert data["summary"]["totalServices"] >= 0
    assert data["summary"]["totalPendingAmount"] >= 0
    assert data["summary"]["totalPaidAmount"] >= 0
