from fastapi import APIRouter, status, Depends, HTTPException
from ATLAS_API.app.telegram.telegram_pydantic import ViewExpenseFilter, SendExpense, AddExpense, DeleteExpense
from sqlalchemy.orm import Session
from ATLAS_API.app.database.database import get_db
from ATLAS_API.app.telegram.utilities.chat_id_verification import chat_id_verification
from typing import List
from ATLAS_API.app.database.models import Expenses
from ATLAS_API.app.telegram.utilities.expense_filter import filter_expense
from sqlalchemy import and_

router = APIRouter(
    prefix="/telegram/web", tags=["telegram web page"] )

@router.post('/expense', status_code=status.HTTP_200_OK, response_model=List[SendExpense])
def expense(expense_filter: ViewExpenseFilter, db: Session = Depends(get_db)):
    chat_id = expense_filter.chat_id
    is_verified, user_db, chat_id, is_admin = chat_id_verification(chat_id, db)
    if is_verified:
        all_expense = filter_expense(expense_filter,db, user_db)
        return all_expense

    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,detail="You are not authorized")


@router.post('/add/expense', status_code=status.HTTP_201_CREATED)
def add_expense(all_expense: List[AddExpense], db: Session = Depends(get_db)):
    total_expense = 0
    for each_expense in all_expense:
        chat_id = each_expense.chat_id
        # It is returning tuple contains the whole row of the user.
        is_verified, user_db, chat_id, is_admin = chat_id_verification(chat_id, db)
        if is_verified:
            # extracting user from table for getting the user_id for the expense table
            user_id = user_db.id

            user_expense = Expenses(user_id=user_id, title=each_expense.title, amount=each_expense.amount,reason=each_expense.reason)
            db.add(user_expense)
            db.commit()
            total_expense += each_expense.amount

    return f'Your amount has been added. Your total expense is: {total_expense}'

@router.delete('/expense/delete')
def expense_delete(expense_detail: DeleteExpense, db: Session = Depends(get_db)):
    chat_id = expense_detail.chat_id
    is_verified, user_db, chat_id, is_admin = chat_id_verification(chat_id, db)

    if is_verified:
        user_id = user_db.id
        # taking out expense from db.
        delete_target = db.query(Expenses).filter(and_(Expenses.id == expense_detail.id, Expenses.user_id == user_id)).delete(synchronize_session=False)
        db.commit()