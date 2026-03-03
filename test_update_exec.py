import requests
import json

base_url = "http://localhost:8000"

# Get an execution ID first
response = requests.get(f"{base_url}/execucoes/")
if response.status_code == 200 and response.json():
    exec_id = response.json()[0]['id']
    print(f"Testing with execution ID: {exec_id}")
    
    # Try to update status as the frontend does
    payload = {
        "producerId": response.json()[0]['producerId'],
        "serviceId": response.json()[0]['serviceId'],
        "date": response.json()[0]['date'],
        "quantity": response.json()[0]['quantity'],
        "totalValue": response.json()[0]['totalValue'],
        "status": "Em Andamento",
        "producerName": response.json()[0]['producerName'],
        "serviceName": response.json()[0]['serviceName'],
        "unit": response.json()[0]['unit']
    }
    
    print(f"Payload: {json.dumps(payload, indent=2)}")
    
    update_response = requests.put(f"{base_url}/execucoes/{exec_id}", json=payload)
    print(f"Status Code: {update_response.status_code}")
    print(f"Response: {update_response.text}")
else:
    print("No executions found or backend down.")
