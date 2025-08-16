#account_data
from models.account import AccountModel
from data.user_data import user_list

# List of accounts to seed into the database

accounts_list = [
    AccountModel(account_id=1,balance=100, currency="USD", user=user_list[0]), #user_id=1
    AccountModel(account_id=2,balance=100, currency="USD", user=user_list[1]), #user_id=2
    AccountModel(account_id=3,balance=100, currency="EUR", user=user_list[2]), #user_id=3
    AccountModel(account_id=4,balance=100, currency="GBP", user=user_list[3]), #user_id=4
    AccountModel(account_id=5,balance=100, currency="USD", user=user_list[4])  #user_id=5
]