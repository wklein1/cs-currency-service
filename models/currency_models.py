from models.custom_base_model import CustomBaseModel

class CurrencyModel(CustomBaseModel):
    code: str
    symbol: str
    name: str
    country: str