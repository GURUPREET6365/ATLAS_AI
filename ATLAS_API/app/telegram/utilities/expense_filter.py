from datetime import datetime
from sqlalchemy import and_
from ATLAS_API.app.database.models import Expenses

# print(datetime.fromisoformat('2026-03-04 00:00:00.000000+05:30'))
def filter_expense(expense_filter, db, user_db):
    if expense_filter.type == 'today':
        from_date = datetime.fromisoformat(expense_filter.from_date)
        to_date = datetime.fromisoformat(expense_filter.to_date)

        expense = db.query(Expenses).filter(and_(Expenses.user_id == user_db.id,Expenses.expense_date >= from_date, Expenses.expense_date < to_date)).all()
        return expense


    elif expense_filter.type == 'date_range':
        from_date = datetime.fromisoformat(expense_filter.from_date)
        to_date = datetime.fromisoformat(expense_filter.to_date)

        expense = db.query(Expenses).filter(and_(Expenses.user_id == user_db.id, Expenses.expense_date >= from_date,
                                                 Expenses.expense_date < to_date)).all()
        return expense

    elif expense_filter.type == 'single_month':
        from_month = datetime.fromisoformat(expense_filter.from_month)
        to_month = datetime.fromisoformat(expense_filter.to_month)

        expense = db.query(Expenses).filter(and_(Expenses.user_id == user_db.id, Expenses.expense_date >= from_month,
                                                 Expenses.expense_date < to_month)).all()
        return expense

    elif expense_filter.type == 'month_range':
        from_month = datetime.fromisoformat(expense_filter.from_month)
        to_month = datetime.fromisoformat(expense_filter.to_month)

        expense = db.query(Expenses).filter(and_(Expenses.user_id == user_db.id, Expenses.expense_date >= from_month,
                                                 Expenses.expense_date < to_month)).all()
        return expense


"""
TODAY:
chat_id=8779748119 type='today' from_date='2026-04-08 00:00:00.000000+05:30' to_date='2026-04-08 19:30:57.431000+05:30' from_month=None to_month=None


DATE RANGE:
chat_id=8779748119 type='date_range' today=None from_date='2026-03-04 00:00:00.000000+05:30' to_date='2026-04-01 23:59:00.000000+05:30' from_month=None to_month=None


SINGLE MONTH:
chat_id=8779748119 type='single_month' today=None from_date=None to_date=None from_month='2026-02-01 00:00:00.000000+05:30' to_month='2026-02-28 23:59:00.000000+05:30'

MONTH RANGE:
chat_id=8779748119 type='month_range' today=None from_date=None to_date=None from_month='2026-01-01 00:00:00.000000+05:30' to_month='2026-05-31 23:59:00.000000+05:30'

"""