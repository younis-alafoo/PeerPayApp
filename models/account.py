#models - account
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from .base import BaseModel

class AccountModel(BaseModel):

    __tablename__ = "accounts"

    account_id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, nullable=False, default=0.0)
    currency = Column(String, default="USD", nullable=False)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)