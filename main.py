from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from decouple import config
import deta

PROJECT_KEY = config("PROJECT_KEY")

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

@app.get(
    "/currencies",
    response_description="Returns list of available currencies",
    description="Get all available currencies.",    
)
async def get_currencies():
    return currenciesDB.fetch().items