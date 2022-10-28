from fastapi.testclient import TestClient
from decouple import config
from main import app

def test_get_currencies_endpoint():
    #ARRANGE
    client = TestClient(app)
    
    expected_currencies_sublist = [
        {
            "code":"EUR",
            "symbol":"€",
            "name":"Euro",
            "country":"European Union"
        }, 
        {
            "code":"COP",
            "symbol":"$",
            "name":"Colombian peso",
            "country":"Colombia"
        }
    ]
    #ACT
    response = client.get("/currencies")
    #ASSERT
    assert response.status_code == 200
    assert response.json() >= expected_currencies_subset