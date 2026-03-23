from ATLAS_API.app.utilities.utilities import send_message
from ATLAS_API.app.database.database import sessionLocal
# creating the db connection, so that I can execute it
import psutil


"""
1. Functions Can Be Stored in Variables
def hello():
    print("Hello")

You can store the function in a variable:

x = hello

Now x points to the function.

Calling it:

x()

Output:

Hello

So:

x -> hello()
"""

class BotCommandsClassifier:
    def __init__(self):
        self.db = sessionLocal()

        self.chat_id = None
        self.commands = {
            "/start":self.start,
            "/expense":self.expense,
            "/battery":self.battery_status,
            "/all_expense":self.all_expense,

            # "/bill": self.bill

        }

    def classify(self, command, chat_id):
        self.chat_id = chat_id
        if command in self.commands:
            return self.commands[command]()
        return None

    # now creating a functions for each commands.

    def start(self):
        help_text = (
            "🚀 * Atlas Assistant Activated * \n\n"
            "Hello Boss! 👋\n"
            "🤖 *Atlas Commands*\n\n"

            "🚀 *Basic Commands*\n"
            "/start - Start the bot / Welcome message\n\n"
            "/expense - Click to see the format of sending the expense.\n\n"
            
            "/battery - Check that battery status.\n\n"
            
            "/all_expense - Check your all expense till now.\n\n"

        )

        send_message(self.chat_id, help_text)

    def expense(self):

        text = ("""
expense
money,reason
money,reason

for extra things like water, gas
expense extra
money,reason

your extra commands are:
'water', 'home', 'market', 'gas', 'electricity'

You can register your fix daily expense, where you can only send 'yourname expense' to mark the fix expense you do, like going to office, coaching, college, etc

"""
        )

        send_message(self.chat_id, text)


    def battery_status(self):
        percent, _, is_charging = psutil.sensors_battery()
        # print(percent, is_charging)
        text = f"your laptop is currently {f'charging and battery is at {int(percent)}%'if is_charging else f'is not charging and at {int(percent)}%'}\n\n"
        send_message(self.chat_id, text)
        # print('message sent')

    def all_expense(self):
        text = ("""
expense.all

and if extra things like milk, expense.all water
just send this command for seeing all the expense you did till now.

your extra commands are:
'water', 'home', 'market', 'gas', 'electricity'

NOTE: for seeing data on specific month or date, or between date, 

Then, send data like:

expense.all
today or specific date

or

date1 
date2

or 

month1
month2

NOTE: Date format should be like: year-month-date
        """)
        send_message(self.chat_id, text)
