import json
from ATLAS_API.app.telegram.utilities.send_message import send_message
from ATLAS_API.app.database.database import sessionLocal
# creating the db connection, so that I can execute it
import psutil
import os
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
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def turn_switch_on():
    send_true()


class BotCommandsClassifier:
    def __init__(self, command, chat_id, is_admin):
        self.is_admin=is_admin
        self.chat_id = chat_id
        self.command = command
        self.all_command = None
        # opening the file of commands
        try:
            file_path = os.path.join(BASE_DIR, 'bot_commands.json')
            with open(file_path, 'r') as f:
                all_commands = json.load(f)
                self.all_command = all_commands

        except FileNotFoundError:
            send_message(self.chat_id, "File For The Commands Not Found From Bot Commands File.")

        except Exception as error:
            send_message(self.chat_id, f'The Error From Bot Commands File Is:\n{error}')


        # initializing database from here, not from the endpoints.
        self.db = sessionLocal()

        self.commands = {
            "/start":self.start,
        
            # ================= EXPENSE ====================
            "/expense":self.expense,
            "/add_expense":self.add_expense,
            "/view_expense":self.view_expense,
        
            # ================= BATTERY AND POWER MODE ====================
            "/battery_and_power_mode":self.battery_and_power_mode,
            "/battery":self.battery_status,
        
            # ================= MICROCONTROLLERS ========================
            "/turn_switch_on": turn_switch_on,
            "/add_user":self.add_user,
            # "/bill": self.bill
        }


    # def classify(self):
    #     print(self.all_command)
    def classify(self, command, chat_id, is_admin):
        self.chat_id=chat_id
        self.is_admin=is_admin
        if command in self.commands:
            self.commands[command]()
        # print(self.all_commands)


    # now creating a functions for each command.
    def start(self):
        help_text = (
            "* Atlas Assistant Activated * \n\n"

            "/start - Start assistant.\n\n"
            
            "/expense - View your expense commands.\n\n"
        
            f"{"/battery_and_power_mode - Check your battery, power mode and control them."if self.is_admin else ''}\n\n"
            
            f"{"/add_user - Add a user to your account."if self.is_admin else ''}\n\n"
            
            f"{"/turn_switch_on - Turn the switch on."if self.is_admin else ''}\n\n"



        )

        send_message(self.chat_id, help_text)

    def expense(self):
        message = (
            "You are at expense page. Manage your expense with below commands.\n\n"
            
            "/view_expense - View your expense.\n\n"
            "/add_expense - Click to send the expense.\n\n"
        )
        send_message(self.chat_id, message)

    def add_expense(self):
        keyboard = [
            [
                {"text": "Open Add Expense Page", "web_app": {"url": "https://atalsai.netlify.app/add-expense.html"}}
            ]
        ]
        send_message(self.chat_id, 'click the button to open the web page', keyboard)

    def view_expense(self):
        keyboard = [
            [
                {"text": "Open View Expense Page", "web_app": {"url": "https://atalsai.netlify.app/expense"}}
            ]
        ]
        send_message(self.chat_id, 'click the button to open the web page', keyboard)

    def battery_and_power_mode(self):
        message = (
            "You are at battery and power mode control page.\nYou can control your power mode, and see battery\n\n"

            "/battery - View your laptop battery status\n\n"

        )
        send_message(self.chat_id, message)

    def battery_status(self):
        percent, _, is_charging = psutil.sensors_battery()
        # print(percent, is_charging)
        text = f"your laptop is currently {f'charging and battery is at {int(percent)}%'if is_charging else f'is not charging and at {int(percent)}%'}\n\n"
        send_message(self.chat_id, text)
        # print('message sent')


    def add_user(self):
        send_message(self.chat_id, "you are in adding user page.")


