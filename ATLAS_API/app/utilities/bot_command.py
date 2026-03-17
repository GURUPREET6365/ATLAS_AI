from ATLAS_API.app.utilities.utilities import send_message

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
        self.chat_id = None
        self.commands = {
            "/help":self.help,
            "/start": self.start,
            # "/all_images": self.all_images,
            # "/all_videos": self.all_videos,
            # "/bill": self.bill
        }

    def classify(self, command, chat_id):
        self.chat_id = chat_id
        if command in self.commands:
            return self.commands[command]()
        return None

    # now creating a functions for each commands.

    def start(self):
        text = ("🚀 *Atlas Assistant Activated*\n\n"
                                "Hello Boss! 👋\n"
                                "I'm fully online and ready to execute your commands.\n\n"
                                "/help — Show all commands\n\n"
                                "💡 _Just send a command and I'll handle the rest._")
        send_message(self.chat_id, text)

    def help(self):
        help_text = (
            "🤖 *Atlas Commands*\n\n"

            "🚀 *Basic Commands*\n"
            "/start - Start the bot / Welcome message\n"
            "/help - Show this help menu\n\n"

            "📂 *Media Commands*\n"
            "/all_images - View all saved images\n"
            "/all_videos - View all saved videos\n"
        )

        send_message(self.chat_id, help_text)