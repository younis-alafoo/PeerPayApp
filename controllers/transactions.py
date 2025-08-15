#Controller - transactions
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from database import get_db
from dependencies.get_current_user import get_current_user
from models import UserModel, AccountModel, TransactionModel, ExchangeRateModel
from serializers.transaction import TransactionSchema
from serializers.account import SendRequest
from datetime import datetime

router = APIRouter()

@router.get("/history", response_model=list[TransactionSchema])
def get_transaction_history(db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):
    
    # load both sender and recipient relationships
    user = (
        db.query(UserModel)
        .options(
            joinedload(UserModel.sent_transactions),
            joinedload(UserModel.received_transactions)
        )
        .filter_by(user_id=current_user.user_id)
        .first()
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Combine both sent and received transactions
    all_transactions = user.sent_transactions + user.received_transactions

    # sort by newest first
    all_transactions.sort(key=lambda tx: tx.created_at, reverse=True)

    #return all_transactions
    return [
    {
        "transaction_id": tx.transaction_id,
        "created_at": tx.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        "sender_acc_id": tx.sender_acc_id,
        "recipient_acc_id": tx.recipient_acc_id,
        "original_amount": tx.original_amount,
        "converted_amount": tx.converted_amount,
        "currency": tx.currency,
        "status": tx.status
    }
    for tx in all_transactions
]

@router.post("/send")
def send_transaction(payload: SendRequest, db: Session = Depends(get_db),current_user: UserModel = Depends(get_current_user)):

        # Get sender's account (assuming only one account per user)
    sender_account = db.query(AccountModel).filter_by(user_id=current_user.user_id).first()
    if not sender_account:
        raise HTTPException(status_code=404, detail="Sender account not found.")

    if payload.recipient_acc_id == sender_account.account_id:
        raise HTTPException(status_code=400, detail="You cannot send money to your own account.")
    
        # Get recipient's account
    recipient_account = db.query(AccountModel).filter_by(account_id=payload.recipient_acc_id).first()
    if not recipient_account:
        raise HTTPException(status_code=404, detail="Recipient account not found.")

        
    recipient_user = db.query(UserModel).filter_by(user_id=recipient_account.user_id).first()
    # Recipient must be a regular user / update - no need because admin does not have account 
    #if not recipient_user or recipient_user.role.lower() != "user":
    #    raise HTTPException(status_code=403, detail="Recipient must be a regular user (not admin).")
    
        #Check sender balance
    if sender_account.balance < payload.amount:
        raise HTTPException(status_code=403, detail="Insufficient funds.")
    
        # Use sender's currency and convert to recipient's currency
    sender_currency = sender_account.currency.upper()
    recipient_currency = recipient_account.currency.upper()

    if sender_currency == recipient_currency:
        rate_value = 1.0
    else:
        rate = db.query(ExchangeRateModel).filter_by(
            base_currency=sender_currency,
            target_currency=recipient_currency
        ).first()
        if not rate:
            raise HTTPException(status_code=404, detail="Exchange rate not found.")
        rate_value = rate.rate

    converted_amount = payload.amount * rate_value

        # Update balances
    sender_account.balance -= payload.amount
    recipient_account.balance += converted_amount

        # Record the transaction
    transaction = TransactionModel(
        sender_acc_id=sender_account.account_id,
        recipient_acc_id=recipient_account.account_id,
        original_amount=payload.amount,
        converted_amount=converted_amount,
        currency=sender_currency,
        status="Success",
        sender_user_id=current_user.user_id,
        recipient_user_id=recipient_user.user_id,
        created_at=datetime.now()
    )

    db.add(transaction)
    db.commit()

    return {
        "message": "Transaction completed successfully.",
        "transaction_id": transaction.transaction_id,
        "converted_amount": round(converted_amount, 2),
        "currency": sender_currency,
        "rate_used": rate_value
    }

@router.get("/transaction/{user_id}", response_model=list[TransactionSchema])
def view_user_transactions(user_id: int, db: Session = Depends(get_db), current_user: UserModel = Depends(get_current_user)):
    
    #Restrict access to admin role
    if current_user.role.lower() != "admin":
        raise HTTPException(status_code=403, detail="Access denied. Admins only.")

    #Fetch the target user
    target_user = db.query(UserModel).filter_by(user_id=user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="User not found.")

    #Load transactions (both sent and received)
    sent = db.query(TransactionModel).filter_by(sender_user_id=user_id).all()
    received = db.query(TransactionModel).filter_by(recipient_user_id=user_id).all()
    all_tx = sent + received

    #Sort newest first
    all_tx.sort(key=lambda tx: tx.created_at, reverse=True)

    return [
        {
            "transaction_id": tx.transaction_id,
            "created_at": tx.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "sender_acc_id": tx.sender_acc_id,
            "recipient_acc_id": tx.recipient_acc_id,
            "original_amount": tx.original_amount,
            "converted_amount": tx.converted_amount,
            "currency": tx.currency,
            "status": tx.status
        }
        for tx in all_tx
    ]