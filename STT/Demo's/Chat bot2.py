class SimpleChatBot:
    def __init__(self):
        self.responses = {
            "hello": "Hi there!",
            "who are you": "I am a chatbot.",
            "how are you": "I'm fine, thank you.",
            "what's your name": "My name is ChatBot.",
            "whats going on": "Nothing much, sir.",
            "who are you ": "I am a chatbot."  # Note: this is the same as an earlier entry
        }

    def get_response(self, user_input):
        # Normalize user input
        user_input = user_input.lower().strip()
        return self.responses.get(user_input, "Sorry, I don't understand that.")

def main():
    bot = SimpleChatBot()
    print("ChatBot: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ['exit', 'quit', 'bye']:
            print("ChatBot: Goodbye!")
            break
        response = bot.get_response(user_input)
        print(f"ChatBot: {response}")

if __name__ == "__main__":
    main()
