from .database import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy import text


class Expenses(Base):
    __tablename__ = 'expenses'

    id = Column(Integer, primary_key=True, nullable=False, index=True)
    user = Column(String, nullable=False)
    amount = Column(Integer, nullable=True)
    reason = Column(String, nullable=True)
    expense_date = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )