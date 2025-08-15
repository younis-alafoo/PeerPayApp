#serializers - transaction
from pydantic import BaseModel
from typing import Optional

class TransactionSchema(BaseModel):
  transaction_id: Optional[int] = True
  created_at: str #datetime
  sender_acc_id: int
  recipient_acc_id: int
  original_amount: float
  converted_amount: float
  currency: str
  status: str

  class Config:
    orm_mode = True