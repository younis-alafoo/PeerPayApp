from models.transaction import TransactionModel
from data.account_data import accounts_list
from data.user_data import user_list

transactions_list = [
    TransactionModel(
        sender_account=accounts_list[0],
        recipient_account=accounts_list[1],
        sender_user=user_list[0],
        recipient_user=user_list[1],
        original_amount=5,
        converted_amount=5,
        currency="USD",
        status="Success"
    ),
    TransactionModel(
        sender_account=accounts_list[2],
        recipient_account=accounts_list[3],
        sender_user=user_list[2],
        recipient_user=user_list[3],
        original_amount=7,
        converted_amount=7,
        currency="USD",
        status="Success"
    ),
    TransactionModel(
        sender_account=accounts_list[4],
        recipient_account=accounts_list[0],
        sender_user=user_list[4],
        recipient_user=user_list[0],
        original_amount=2.5,
        converted_amount=2.5,
        currency="USD",
        status="Success"
    )
]