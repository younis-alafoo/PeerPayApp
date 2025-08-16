from sqlalchemy.orm import sessionmaker
from models.base import Base
from data.account_data import accounts_list
from data.transaction_data import transactions_list
from data.user_data import user_list
from data.exchange_rate_data import exchange_rates
from config.environment import db_URI
from sqlalchemy import create_engine
from sqlalchemy import text

engine = create_engine(db_URI)
SessionLocal = sessionmaker(bind=engine)

try:
    print("Recreating database...")
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    print("Seeding the database...")
    db = SessionLocal()

    # Seed users first, as accounts and transactions depend on it
    db.add_all(user_list)
    db.commit()

    # then Seed accounts, as transactions depend on it
    db.add_all(accounts_list)
    db.commit()

    # Seed transactions after accounts
    db.add_all(transactions_list)
    db.commit()

    # Seed exchange_rates
    db.add_all(exchange_rates)
    db.commit()

    db.execute(text("ALTER SEQUENCE users_user_id_seq RESTART WITH 7"))  # There are 6 records in users table to avoid user_id duplication
    db.execute(text("ALTER SEQUENCE accounts_account_id_seq RESTART WITH 6")) #There are 5 records in accounts table to avoid account_id duplication
    db.commit()

    db.close()

    print("Database seeding complete!")
except Exception as e:
    print("An error occurred:", e)