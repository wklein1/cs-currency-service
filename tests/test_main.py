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
    assert all(currencie in response.json() for currencie in expected_currencies_sublist)


def test_get_currency_exchange_rate():
    #ARRANGE
    client = TestClient(app)
    
    expected_key = "exchangeRate"
    #ACT
    response = client.get("/currencies/EUR/JPN")
    #ASSERT
    assert response.status_code == 200
    assert response.json()[expected_key]