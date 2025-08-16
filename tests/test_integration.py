from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_login_success():
    response = client.post("/users/login", json={
        "username": "aa",
        "password": "securepassword2"
    })
    assert response.status_code == 200
    data = response.json()
    assert "token" in data
    assert data["message"] == "Login successful"

def test_login_failure_():
    response = client.post("/users/login", json={
        "username": "aa",
        "password": "wrongpassword"
    })
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Invalid username or password"


def test_get_my_account():
    # Login as user "bb"
    login_res = client.post("/users/login", json={
        "username": "bb",
        "password": "securepassword3"
    })
    assert login_res.status_code == 200
    token = login_res.json()["token"]

    # Call /accounts/me with token
    res = client.get("/accounts/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    data = res.json()

    assert data["account_id"] == 2
    assert data["currency"] == "USD"
    assert "balance" in data

def test_get_current_user_details():
    # Login as user "ee"
    login_res = client.post("/users/login", json={
        "username": "ee",
        "password": "securepassword6"
    })
    assert login_res.status_code == 200
    token = login_res.json()["token"]

    # Call /users/me with token
    res = client.get("/users/me", headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    data = res.json()

    # Check user details
    assert data["username"] == "ee"
    assert data["email"] == "eli.evans@email.com"
    assert data["account_id"]  == 5

def test_transaction_history():
    # Login as user "cc"
    login_res = client.post("/users/login", json={
        "username": "cc",
        "password": "securepassword4"
    })
    assert login_res.status_code == 200
    token = login_res.json()["token"]

    # Call /transactions/history with token
    res = client.get("/transactions/history", headers={
        "Authorization": f"Bearer {token}"
    })
    assert res.status_code == 200
    data = res.json()

    # Check the seeded transaction
    if data:
        tx = data[0]
        assert "transaction_id" in tx
        assert "created_at" in tx
        assert tx["sender_acc_id"] == 3
        assert tx["recipient_acc_id"] == 4
        assert tx["status"] == "Success"
        assert tx["currency"] == "EUR"
        assert tx["original_amount"] == 7
        assert tx["converted_amount"] == 5.95

def test_admin_can_view_user_transactions():
    # Login as admin
    login_res = client.post("/users/login", json={
        "username": "Yunis",
        "password": "securepassword1"
    })
    assert login_res.status_code == 200
    token = login_res.json()["token"]

    # Target user ID (user "ee" has user_id = 5)
    user_id = 5

    # Call /transactions/{user_id} with admin token
    res = client.get(f"/transactions/transaction/{user_id}", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200
    data = res.json()
    
    # Check the seeded transaction
    if data:
        tx = data[0]
        assert "transaction_id" in tx
        assert "created_at" in tx
        assert tx["sender_acc_id"] == 5
        assert tx["recipient_acc_id"] == 1
        assert tx["status"] == "Success"
        assert tx["currency"] == "USD"
        assert tx["original_amount"] == 2.5
        assert tx["converted_amount"] == 2.5

def test_non_admin_cannot_view_user_transactions():
    # Login as user "bb"
    login_res = client.post("/users/login", json={
        "username": "bb",
        "password": "securepassword3"
    })
    assert login_res.status_code == 200
    token = login_res.json()["token"]

    # Try to access another user's transactions
    user_id = 1

    res = client.get(f"/transactions/transaction/{user_id}", headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 403
    assert res.json()["detail"] == "Access denied. Admins only."

def test_send_transaction():
    # Login as sender "aa"
    login_res = client.post("/users/login", json={
        "username": "aa",
        "password": "securepassword2"
    })
    assert login_res.status_code == 200
    token = login_res.json()["token"]

    # Send transaction to account_id 4 -> user "dd"
    res = client.post("/transactions/send", json={
        "recipient_acc_id": 4,
        "amount": 3
    }, headers={
        "Authorization": f"Bearer {token}"
    })

    assert res.status_code == 200
    data = res.json()

    # Check the transaction
    assert data["message"] == "Transaction completed successfully."
    assert "transaction_id" in data
    assert data["converted_amount"] == 2.34
    assert data["currency"] == "USD"
    assert data["rate_used"] == .78