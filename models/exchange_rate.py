from sqlalchemy import Column, Integer, String, Float
from .base import BaseModel

class ExchangeRateModel(BaseModel):
    __tablename__ = "exchange_rates"

    id = Column(Integer, primary_key=True, index=True)
    base_currency = Column(String(3), nullable=False)
    target_currency = Column(String(3), nullable=False)
    rate = Column(Float, nullable=False)