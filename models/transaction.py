#models - transaction
from sqlalchemy import Column, Integer, String, ForeignKey, Float
from .base import BaseModel

class TransactionModel(BaseModel):

    __tablename__ = "transactions" 

    transaction_id = Column(Integer, primary_key=True, index=True)  # Unique identifier for the transaction
    sender_acc_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    recipient_acc_id = Column(Integer, ForeignKey("accounts.account_id"), nullable=False)
    original_amount = Column(Float, nullable=False, default=0.0)
    converted_amount = Column(Float, nullable=False, default=0.0)
    currency = Column(String, default="USD", nullable=False)
    status = Column(String, nullable=False) 
    sender_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    recipient_user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)