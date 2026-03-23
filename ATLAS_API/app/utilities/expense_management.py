from ATLAS_API.app.utilities.utilities import send_message
from ATLAS_API.app.utilities.date_parser import command_date_parser
from ATLAS_API.app.database.models import Expenses
from ATLAS_API.app.database.database import sessionLocal


# Checking that the user sent the message is for the expense or not?
class ExpenseManagement:
    def __init__(self):
        self.all_expense = None
        self.chat_id = None
        self.amount = None
        self.reason = None
        self.username = None
        self.db = sessionLocal()

    def check_expense_message(self, data, chat_id, username):
        self.chat_id = chat_id
        self.username=username
        # splitting the data with comma
        split_data = data.split('\n')
        print(split_data)
        # taking the first element that contains the data of expense
        command = split_data[0].strip().lower().split(' ')
        print(command)

        list_extra_things = ['water', 'home', 'market', 'gas', 'electricity']
        """
        I am making the command like when command:
        expense: Then add the default or add the data sent.
        expense all: Then show the expense.
        expense extra: This is for home, market, milk, water, electricity, gas, 
        expense all extra: This is for the showing the extra things details.
        """
        # The 0 index will always have command.
        if command[0] == "expense":

            # Checking that user also sent any other data or not?
            # This is for multiple data

            # Here I am checking that the expense came is for the extras or not, if not then go, and if yes then go to extras func.
            if len(split_data) > 1 and command[1] not in list_extra_things:
                # we are making new list where the username_expense element has been removed. It means make new list
                # from split_data list contains from element 1 to end
                self.all_expense = split_data[1:]

                # send_message(chat_id, "Found the expense.")
                self.add_expense()
                return True

            # This is for the normal expenses/default only expenses
            elif command[1] in list_extra_things:
                self.username = command[1]
                self.all_expense = split_data[1:]
                # send_message(chat_id, f"Found the expense of {self.username}.")
                self.add_expense()
                return True

            else:
                # print('entering here......')
                if username == 'gurupreet':
                    self.amount = 84
                    self.reason = 'coaching'

                elif username == 'water':
                    self.amount = 15
                    self.reason = 'water'

                # send_message(chat_id, "Found the expense of default.")
                self.add_expense()
                return True

        # This condition is for the seeing all expenses.
        # This is because expense show command will be, ['expense', 'all', 'milk']

        elif command[0]== 'expense.all':
            # we are taking the date from index 1 that second data to end
            # checking that the length of the command ['expense.all', 'water'] i.e this will be mostly two, if with date then the split data will have more length
            if len(command) > 1:
                self.username = command[1]
                self.overall_expense()
                return True
            self.overall_expense()

            return True

        else:
            return False
    def add_expense(self):
        db = self.db

        # yaha pe ek error aa sakta hai ki jab default expense save karna hai to yaha pe self.all_expense none rahega, so hame condition lagana hai, kyunki none type can't be iterable.
        if self.all_expense is not None:
            total_expense = 0
            for expense in self.all_expense:
                # ['500:metro card recharge', '250: eating']
                try:
                    each_expense = expense.split(',')
                    amount = each_expense[0].strip()
                    total_expense += int(amount)
                    self.amount = amount
                    reason = each_expense[1].strip()
                    self.reason = reason
                    new_expense = Expenses(user=self.username, amount=self.amount, reason=self.reason)
                    db.add(new_expense)
                    db.commit()
                except ValueError:
                    send_message(self.chat_id, "Please enter a valid amount, valid amount added to the database, non-valid amount is not added.")

            send_message(self.chat_id, f"{self.username}'s expenses has been added to database\nYour total expense is: {total_expense}")
            return True

        else:
            total_expense = self.amount
            new_expense = Expenses(user=self.username, amount=self.amount, reason=self.reason)
            db.add(new_expense)
            db.commit()
            send_message(self.chat_id, f"{self.username}'s default expenses has been added to database\nYour total expense is: {total_expense}")
            return True

    def overall_expense(self):
        db = self.db
        expense_list = []
        expenses = db.query(Expenses).filter(Expenses.user == self.username).all()
        if expenses:

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

        else:

            send_message(self.chat_id, f"oops! there is no any expense found for {self.username}")
        return True