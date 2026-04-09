from ATLAS_API.app.telegram.utilities.send_message import send_message
from ATLAS_API.app.database.database import sessionLocal
# creating the db connection, so that I can execute it
import psutil
from ATLAS_API.app.micro_controller.mqtt_pico import send_true


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
Hell
So:
x -> hello()
"""


def turn_switch_on():
    send_true()


class BotCommandsClassifier:
    def __init__(self):
        # initializing database from here, not from the endpoints.
        self.db = sessionLocal()

        self.is_admin=False
        self.chat_id = None
        self.commands = {
            "/start":self.start,
            "/add_expense":self.add_expense,
            "/battery":self.battery_status,
            "/view_expense":self.view_expense,
            "/add_user":self.add_user,
            "/turn_switch_on": turn_switch_on,
            # "/bill": self.bill
        }

    def classify(self, command, chat_id, is_admin):
        print(command)
        self.chat_id = chat_id
        self.is_admin=is_admin
        if command in self.commands:
            self.commands[command]()


    # now creating a functions for each command.
    def start(self):
        help_text = (
            "🚀 * Atlas Assistant Activated * \n\n"
            "Hello Boss! 👋\n"
            "🤖 *Atlas Commands*\n\n"

            "🚀 *Basic Commands*\n"
            "/start - Start the bot / Welcome message\n\n"
            "/add_expense - Click to send the expense.\n\n"
            
            "/battery - Check that battery status.\n\n"
            
            "/view_expense - View your expense.\n\n"
            
            f"{"/add_user - Add a user to your account."if self.is_admin else ''}\n\n"
            
            f"{"/turn_switch_on - Turn the switch on."if self.is_admin else ''}\n\n"



        )

        send_message(self.chat_id, help_text)

    def add_expense(self):
        keyboard = [
            [
                {"text": "Open Add Expense Page", "web_app": {"url": "https://atalsai.netlify.app/add-expense.html"}}
            ]
        ]
        send_message(self.chat_id, 'click the button to open the web page', keyboard)


    def battery_status(self):
        percent, _, is_charging = psutil.sensors_battery()
        # print(percent, is_charging)
        text = f"your laptop is currently {f'charging and battery is at {int(percent)}%'if is_charging else f'is not charging and at {int(percent)}%'}\n\n"
        send_message(self.chat_id, text)
        # print('message sent')

    def view_expense(self):
        keyboard = [
            [
                {"text": "Open View Expense Page", "web_app": {"url": "https://atalsai.netlify.app/expense"}}
            ]
        ]
        send_message(self.chat_id, 'click the button to open the web page', keyboard)

    def add_user(self):
        send_message(self.chat_id, "you are in adding user page.")


