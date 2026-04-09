from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime, date
from typing import Optional


# ======================= RECEIVING =====================

class ViewExpenseFilter(BaseModel):
    chat_id:int
    type: str
    from_date: Optional[str] = None
    to_date: Optional[str] = None
    from_month: Optional[str] = None
    to_month: Optional[str] = None


class AddExpense(BaseModel):
    chat_id: int
    title: Optional[str] = None
    amount: int
    reason: str


# ===================== SENDING ================================

class SendExpense(BaseModel):
    title: Optional[str] = None
    amount:int
    reason:str
    expense_date:datetime

    # This allows Pydantic to read 'Expenses' object attributes directly
    model_config = ConfigDict(from_attributes=True)

