#serializers - account
from pydantic import BaseModel, Field
from typing import Optional

class AccountSchema(BaseModel):
  account_id: Optional[int] = True
  balance: float
  currency: str

  class Config:
    orm_mode = True

class SendRequest(BaseModel):
    recipient_acc_id: int
    amount: float = Field(gt=0, description="Amount must be greater than zero")
    #currency: str = Field(min_length=3, max_length=3, description="Three-letter currency code (e.g. 'USD')")

    class Config:
      orm_mode = True