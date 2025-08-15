#account_data
from models.account import AccountModel
from data.user_data import user_list

# List of accounts to seed into the database

accounts_list = [
    AccountModel(balance=10, currency="USD", user=user_list[0]), #user_id=2
    AccountModel(balance=10, currency="USD", user=user_list[1]), #user_id=3
    AccountModel(balance=10, currency="EUR", user=user_list[2]), #user_id=4
    AccountModel(balance=10, currency="GPB", user=user_list[3]), #user_id=5
    AccountModel(balance=10, currency="USD", user=user_list[4])  #user_id=6
]