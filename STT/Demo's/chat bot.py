from chatterbot import ChatBot
from chatterbot.trainers import ChatterBotCorpusTrainer

# Create a new ChatBot instance
chatbot = ChatBot('MyChatBot')

# Create a new trainer for the ChatBot
trainer = ChatterBotCorpusTrainer(chatbot)

# Train the chatbot based on the english corpus
trainer.train('chatterbot.corpus.english')

# Main loop to interact with the chatbot
if __name__ == "__main__":
    print("Type 'quit' to exit")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'quit':
            break
        response = chatbot.get_response(user_input)
        print(f"Bot: {response}")
