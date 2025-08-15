#models -  __int__
from .base import BaseModel, Base
from .user import UserModel
from .account import AccountModel
from .transaction import TransactionModel
from .exchange_rate import ExchangeRateModel
from sqlalchemy.orm import relationship

__all__ = ["BaseModel", "Base", "UserModel", "AccountModel", "TransactionModel", "ExchangeRateModel"]

# Relationship bindings (after all models are defined)

# User - Accounts
UserModel.accounts = relationship("AccountModel", back_populates="user")
AccountModel.user = relationship("UserModel", back_populates="accounts")

# User - Transactions
UserModel.sent_transactions = relationship("TransactionModel", foreign_keys=[TransactionModel.sender_user_id], back_populates="sender_user")
UserModel.received_transactions = relationship("TransactionModel", foreign_keys=[TransactionModel.recipient_user_id], back_populates="recipient_user")
TransactionModel.sender_user = relationship("UserModel", foreign_keys=[TransactionModel.sender_user_id], back_populates="sent_transactions")
TransactionModel.recipient_user = relationship("UserModel", foreign_keys=[TransactionModel.recipient_user_id], back_populates="received_transactions")

# Account - Transactions
AccountModel.sender_transactions = relationship("TransactionModel", foreign_keys=[TransactionModel.sender_acc_id], back_populates="sender_account")
AccountModel.recipient_transactions = relationship("TransactionModel", foreign_keys=[TransactionModel.recipient_acc_id], back_populates="recipient_account")
TransactionModel.sender_account = relationship("AccountModel", foreign_keys=[TransactionModel.sender_acc_id], back_populates="sender_transactions")
TransactionModel.recipient_account = relationship("AccountModel", foreign_keys=[TransactionModel.recipient_acc_id], back_populates="recipient_transactions")