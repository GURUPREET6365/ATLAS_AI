from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import text


class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=True)
    user = Column(String, nullable=False)
    amount = Column(Integer, nullable=True)
    reason = Column(String, nullable=True)
    expense_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=True)
    email = Column(String, nullable=False, unique=True)
    role = Column(String, nullable=False)
    chat_id = Column(String, nullable=True)
    password = Column(String, nullable=False)
    phone_number = Column(String, nullable=False, unique=True)
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )