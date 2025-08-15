#models - base
from sqlalchemy import Column, DateTime, func
from sqlalchemy.ext.declarative import declarative_base

#base class for all models
Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True 

    created_at = Column(DateTime, default=func.now())  # Timestamp for record creatation
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())  # Timestamp for record updation