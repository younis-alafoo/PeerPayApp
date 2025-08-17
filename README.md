# PeerPayApp 💸 Project 

PeerPayApp is a lightweight peer-to-peer transaction platform that allows users to register, log in, view account details, and securely send money to other users. It includes a dedicated admin dashboard for monitoring user transactions.

---

Tables Overview:

| Table          | Description                                                                 |
|----------------|-----------------------------------------------------------------------------|
| users          | Stores user profiles and credentials (with roles: User, Admin)              |
| accounts       | Each user has one account holding balance and currency                      |
| transactions   | Logs all transfers between accounts, including currency conversion tracking |
| exchange_rates | Stores exchange rates between supported currencies (USD, EUR, GBP)          |

---

Entity Relationships:

- **User ↔ Account**:  
  - One-to-One (users.user_id → accounts.user_id)  
  - A user has one primary account with a specified currency and balance.

- **User ↔ Transaction**:  
  - One-to-Many:  
    - users.user_id → transactions.sender_user_id  
    - users.user_id → transactions.recipient_user_id  
  - Users can send and receive many transactions.

- **Account ↔ Transaction**:  
  - One-to-Many:  
    - accounts.account_id → transactions.sender_acc_id  
    - accounts.account_id → transactions.recipient_acc_id  
  - Account could have many transactions as sender and recipient.

---

Route Documentation:

| Route                    | HTTP Method | who can Access? | Description                                                          				| Parameters   |
|--------------------------|-------------|-----------------|----------------------------------------------------------------------------------------------------|--------------|
| /                        | GET         | Public	   | The home route                                                       				| None         |
| /register		   | POST	 | Public	   | Registers a new user with required currency selection (USD, EUR, or GBP). Automatically creates a 	| None	       |
|			   |		 | 		   | linked account. Stores hashed password.								|	       |
| /login		   | POST	 | Public 	   | Authenticates the user and returns a JWT token.			  				| None	       |
| /users/me                | GET         | Logged-in users | Returns information about the currently authenticated user, including:  				| None         |
|			   |		 |		   | username, email, and linked account ID.								|	       |
| /accounts/me		   | GET         | Logged-in users | Returns current user's account details (account id, currency, and balance). 			| None         |
| /transactions/send       | POST        | Logged-in users | Transfers money from the current user to another user by specifying the recipient’s account ID and | None	       |
|			   |		 |		   | the amount. Prevents overdrafts and Automatically applies exchange rates when currencies differ.	|	       |
| /transactions/history    | GET         | Logged-in users | Returns a list of current user’s transactions both sent and received sorted by transaction date.	| None	       |
| /transactions/{user_id}  | GET         | Admins only	   | Retrieves all transactions (sent + received) for any user by user ID.				| user_id (int)|

---

## 🚀 Getting Started

### 1. Clone the Repository
https://github.com/younis-alafoo/PeerPayApp.git

### 2. Set Up the Environment
Create & Activate a Virtual Environment
 python -m venv venv
 venv\Scripts\activate

### 3. Install dependencies:
pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic passlib pyjwt pytest starlette httpx selenium


### 4. Configure the Database:
Update config/environment.py with your PostgreSQL connection string:
Run the seeding script to initialize test data (python seed.py)


### 5. Start the Backend Server:
uvicorn main:app --reload

### 6. Running Tests:
unit test: pytest tests/test_unit.py
integration test: pytest tests/test_integration.py
E2E test: pytest tests/test_e2e.py

### 7. URL's
Access the API at: http://localhost:8000
Interactive docs: http://localhost:8000/docs
Login Page: http://localhost:8000/static/frontend/login.html
Register Page: http://localhost:8000/static/frontend/register.html
Account Page: http://localhost:8000/static/frontend/account.html
Transactions Page: http://localhost:8000/static/frontend/transactions.html
Admin Page: http://localhost:8000/static/frontend/admin.html

--- 

## 🛠️ Technologies and Libraries Used: 

FastAPI, unicorn, SQLAlchemy, PostgreSQL, pytest, httpx, selenium, HTML/CSS, JavaScript, pyjwt, pydantic, uuid, Starlette, passlib, bcrypt, psycopg2-binary