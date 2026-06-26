from fastapi.testclient import TestClient
from fastapi import status
import main

client = TestClient(main.app)

def test_health_check():

    response = client.get("/health-check")
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"status": "healthy"}

