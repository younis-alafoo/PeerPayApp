#serializers - user
from pydantic import BaseModel, Field, validator
#from .account import AccountSchema

class UserSchema(BaseModel):
    username: str  #unique username
    #role: str
    full_name: str
    email: str
    currency: str = Field(..., description="Account currency: USD, EUR, or GBP")
    password: str
    
    @validator("currency")
    def validate_currency(cls, value):
        allowed = {"USD", "EUR", "GBP"}
        currency_upper = value.upper()
        if currency_upper not in allowed:
            raise ValueError(f"Currency must be one of {', '.join(allowed)}")
        return currency_upper


    class Config:
        orm_mode = True

class UserResponseSchema(BaseModel):
    username: str
    email: str
    #account: AccountSchema

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    username: str
    password: str

class UserToken(BaseModel):
    token: str  #generated JWT token after the successful login
    message: str

    class Config:
        orm_mode = True