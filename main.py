from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
from modules.csv import csv_reader
from models import currency_models, error_models
import requests
import deta

PROJECT_KEY = config("PROJECT_KEY")
EXCHANGE_RATE_API_KEY = config("EXCHANGE_RATE_API_KEY")

deta = deta.Deta(PROJECT_KEY)
currenciesDB = deta.Base("currencies")

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)

currencies = csv_reader.read_csv("currencies.csv")


def insert_currencies_in_db(currencies:list[currency_models.CurrencyModel]):   
    for currencie in currencies:
        try:
            currenciesDB.insert(currency_models.CurrencyModel(**currencie).dict())
        except Exception as ex:
            print(f"{currencie['name']} is already in db!")
        

insert_currencies_in_db(currencies)

@app.get(
    "/currencies",
    response_model=list[currency_models.CurrencyModel],
    response_description="Returns list of available currencies",
    responses={503 :{
            "model": error_models.HTTPErrorModel,
            "description": "Error raised if database request fails."
        }},
    description="Get all available currencies.",    
)
async def get_currencies():
    try:
        return currenciesDB.fetch().items
    except:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail="Error while connecting to database")

def forward_request(old_currency,new_currency):

    url = f"https://currencyapi.net/api/v1/rates?key={EXCHANGE_RATE_API_KEY}&output=JSON"
    
    response = requests.request("GET", url)
    rates_obj = response.json()

    old_to_usd = 1/rates_obj["rates"][old_currency]
    old_to_new = old_to_usd * rates_obj["rates"][new_currency]
    exchange_obj = {"exchange_rate":old_to_new}

    return exchange_obj


@app.get(
    "/currencies/{old_currency_code}/{new_currency_code}",
    response_model=currency_models.ExchangeRateResponseModel,
    response_description="Returns exchangerate from old currency to new",
    description="Get exchangerate from old currency to new.",    
)
async def get_currency_exchange_rate(old_currency_code, new_currency_code):
    return forward_request(old_currency_code, new_currency_code)



