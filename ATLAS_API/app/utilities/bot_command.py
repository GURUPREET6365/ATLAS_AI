from ATLAS_API.app.utilities.utilities import send_message
from ATLAS_API.app.database.database import sessionLocal
# creating the db connection, so that I can execute it



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
            "/expense":self.expense

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
        )

        send_message(self.chat_id, help_text)

    def expense(self):

        text = ("""
yourname expense
money:reason
money:reason

You can register your fix daily expense, where you can only send 'yourname expense' to mark the fix expense you do, like going to office, coaching, college, etc

NOTE: Don't use comma or anything.
"""
        )

        send_message(self.chat_id, text)