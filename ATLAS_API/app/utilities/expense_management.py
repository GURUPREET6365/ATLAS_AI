from ATLAS_API.app.utilities.utilities import send_message, GURUPREET_CHAT_ID
from ATLAS_API.app.database.models import Expenses
from ATLAS_API.app.database.database import sessionLocal


# Checking that the user sent the message is for the expense or not?
class ExpenseManagement:
    def __init__(self):
        self.all_expense = None
        self.chat_id = None
        self.amount = None
        self.reason = None
        self.db = sessionLocal()

    def check_expense_message(self, data, chat_id):
        self.chat_id = chat_id
        # splitting the data with comma
        split_data = data.split('\n')
        # print(split_data)
        # taking the first element that contains the data of expense
        user_name_expense = split_data[0].strip().lower()

        add_expense_list = ["gurupreet expense","jyoti expense", "gurumeet expense", 'market expense', "archana expense"]

        check_expense_list = ["gurupreet expense all","jyoti expense all", "gurumeet expense all", 'market expense all', "archana expense all", "market expense all"]
        if user_name_expense in add_expense_list:

            username = user_name_expense.replace(" expense", "")

            # Checking that user also sent any other data or not?
            if len(split_data) > 1:
                print('i am here')
                # we are making new list where the username_expense element has been removed. It means make new list
                # from split_data list contains from element 1 to end
                self.all_expense = split_data[1:]

                # send_message(chat_id, "Found the expense.")
                self.add_expense(username)
                return True
            # This is for the normal expenses/default only expenses
            else:
                # print('entering here......')
                if username == 'gurupreet':
                    self.amount = 84
                    self.reason = 'coaching'

                self.add_expense(username)

                return True

        # This condition is for the seeing all expenses.
        elif user_name_expense in check_expense_list:
            username = user_name_expense.split(" ")[0]
            # print(username)
            self.overall_expense(username)

            return True

        else:
            return False
    def add_expense(self, username):
        db = self.db

        # yaha pe ek error aa sakta hai ki jab default expense save karna hai to yaha pe self.all_expense none rahega, so hame condition lagana hai, kyunki none type can't be iterable.
        if self.all_expense is not None:
            total_expense = 0
            for expense in self.all_expense:
                # ['500:metro card recharge', '250: eating']
                each_expense = expense.split(':')
                amount = each_expense[0].strip()
                try:
                    total_expense += int(amount)
                    self.amount = amount
                    reason = each_expense[1].strip()
                    self.reason = reason
                    new_expense = Expenses(user=username, amount=self.amount, reason=self.reason)
                    db.add(new_expense)
                    db.commit()
                except ValueError:
                    send_message(self.chat_id, "Please enter a valid amount, valid amount added to the database, non-valid amount is not added.")



            send_message(self.chat_id, f"{username}'s expenses has been added to database\nYour total expense is: {total_expense}")
            return True

        else:
            total_expense = self.amount
            new_expense = Expenses(user=username, amount=self.amount, reason=self.reason)
            db.add(new_expense)
            db.commit()
            send_message(self.chat_id, f"{username}'s default expenses has been added to database\nYour total expense is: {total_expense}")
            return True

    def overall_expense(self, username):
        db = self.db
        expense_list = []
        expenses = db.query(Expenses).filter(Expenses.user == username).all()
        total_expense = 0
        for index, each_expense in enumerate(expenses):
            date = each_expense.expense_date
            date_str = date.date().isoformat()
            # adding expense
            total_expense += each_expense.amount
            data = f"{index+1}. {each_expense.reason} = ₹{each_expense.amount} | {date_str}"
            expense_list.append(data)
        # joining list's element as a string.
        result = ",\n\n".join(expense_list)

        send_message(self.chat_id, f"{result}\n\nTotal expense is = ₹{total_expense}")
        return True