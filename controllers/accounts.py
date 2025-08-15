#Controller - accounts
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from serializers.account import AccountSchema
from database import get_db
from dependencies.get_current_user import get_current_user
from models import UserModel

router = APIRouter()

from sqlalchemy.orm import joinedload

@router.get("/me", response_model=AccountSchema)
def get_my_account(db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    
    user = db.query(UserModel).filter_by(user_id=current_user.user_id).first()
    
    if not user or not user.accounts:
        raise HTTPException(status_code=404, detail="No account found for this user")
    
    account = user.accounts[0] #if user.accounts else None

    return {
        #"username": user.username,
        "account_id": account.account_id,
        "balance": account.balance,
        "currency": account.currency
    }
