from ATLAS_API.app.utilities.utilities import send_message
from ATLAS_API.app.database.models import Expenses
from ATLAS_API.app.database.database import sessionLocal

# Checking that the user sent the message is for the expense or not?
class ExpenseManagement:
    def __init__(self):
        self.all_expense = None
        self.chat_id = None
        self.amount = None
        self.reason = None

    def check_expense_message(self, data, chat_id):
        self.chat_id = chat_id
        # splitting the data with comma
        split_data = data.split('\n')

        # taking the first element that contains the data of expense
        user_name_expense = split_data[0].strip()
        if user_name_expense.lower() == "gurupreet expense" or user_name_expense.lower() == "jyoti expense" or user_name_expense.lower() == "archana expense" or user_name_expense.lower() == "gurumeet expense":

            username = user_name_expense.lower().replace(" expense", "")

            # Checking that user also sent any other data or not?
            if len(split_data) > 1:
                # we are making new list where the username_expense element has been removed. It means make new list
                # from split_data list contains from element 1 to end
                self.all_expense = split_data[1:]

                # send_message(chat_id, "Found the expense.")
                self.add_expense(username)
                return True
            # This is for the normal expenses/default only expenses
            else:
                if username == 'gurupreet':
                    self.amount = 84
                    self.reason = 'coaching'

                self.add_expense(username)

                return True

        else:
            return False
    def add_expense(self, username):
        db = sessionLocal()

        # print(username)
        # print(self.chat_id)
        # print(self.all_expense)

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



            send_message(self.chat_id, f"Your expense has been added to database\nYour total expense is: {total_expense}")
            return True

        else:
            new_expense = Expenses(user=username, amount=self.amount, reason=self.reason)
            db.add(new_expense)
            db.commit()
            send_message(self.chat_id, "Your default expense has been added to database")

