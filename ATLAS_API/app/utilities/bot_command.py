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
        send_message(self.chat_id, "🚀 *Atlas Assistant Activated*\n\n"
                                "Hello Boss! 👋\n"
                                "I'm fully online and ready to execute your commands.\n\n"
                                "⚙️ *Capabilities*\n"
                                "• Fetch images and videos\n"
                                "• Generate bills\n"
                                "• Answer questions\n"
                                "• Execute automation tasks\n\n"
                                "📜 *Available Commands*\n"
                                "/start — Initialize assistant\n"
                                "/all_images — Get all images\n"
                                "/all_videos — Get all videos\n"
                                "/bill — Generate bill\n"
                                "/help — Show all commands\n\n"
                                "💡 _Just send a command and I'll handle the rest._")


