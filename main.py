#main
from fastapi import FastAPI
from controllers.accounts import router as AccountsRouter
from controllers.transactions import router as TransactionsRouter
from controllers.users import router as UsersRouter
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/static", StaticFiles(directory=".", html=True), name="static")

app.include_router(AccountsRouter, prefix="/accounts")
app.include_router(TransactionsRouter, prefix="/transactions")
app.include_router(UsersRouter, prefix="/users")

@app.get('/')
def home():
    return 'Hello World!'