#Controller - users
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from serializers.user import UserSchema, UserLogin, UserToken, UserResponseSchema
from database import get_db
from dependencies.get_current_user import get_current_user
from models import UserModel, AccountModel

router = APIRouter()

@router.post("/register", response_model=UserResponseSchema)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    # Check if the username or email already exists
    existing_user = db.query(UserModel).filter(
        (UserModel.username == user.username) | (UserModel.email == user.email)
    ).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username or email already exists")

    new_user = UserModel(username=user.username, role="User", full_name=user.full_name, email=user.email)
    # Use the set_password method to hash the password
    new_user.set_password(user.password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    account = AccountModel(
        user_id=new_user.user_id,
        balance=0.0,
        currency=user.currency
    )
    db.add(account)
    db.commit()

    return new_user

@router.post("/login", response_model=UserToken)
def login(user: UserLogin, db: Session = Depends(get_db)):

    # Find the user by username
    db_user = db.query(UserModel).filter(UserModel.username == user.username).first()

    # Check if the user exists and if the password is correct
    if not db_user or not db_user.verify_password(user.password):
        raise HTTPException(status_code=400, detail="Invalid username or password")

    # Generate JWT token
    token = db_user.generate_token()

    # Return token and a success message
    return {"token": token, "message": "Login successful"}

@router.get("/me")
def get_current_user_details(
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(get_current_user)
):
    user = db.query(UserModel).filter_by(user_id=current_user.user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    account = user.accounts[0] if user.accounts else None

    return {
        "username": user.username,
        "email": user.email,
        "account_id": account.account_id if account else None
    }