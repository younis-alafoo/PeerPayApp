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

-Clone the Repository: "https://git.generalassemb.ly/yunis/PeerPay-Project.git"
-Create & Activate a Virtual Environment, Install Dependencies:
 pip install fastapi uvicorn sqlalchemy psycopg2-binary pydantic passlib pyjwt
 pip install pytest starlette httpx
-Run the Application: "uvicorn main:app --reload"
Access the API at: http://localhost:8000
Interactive docs: http://localhost:8000/docs

--- 

Technologies used: FastAPI, SQLAlchemy, PostgreSQL, and PyTest.




