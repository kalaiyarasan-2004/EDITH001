import nltk
import random
import jarvis
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyaudio
# Example conversation pairs


recognizer = sr.Recognizer()
engine = pyttsx3.init()
conversations = [
    ("Hello", "Hi there!"),
    ("who are you ", "iam denver"),
    ("How are you?", "I'm fine, thank you."),
    ("What's your name?", "My name is denver."),
    ("whats going on", "nothing sir"),
    ("who are you ", "iam denver"),
("Hello", "Hi there!"),
("Hi", "Hello! How can I assist you today?"),
("Hey", "Hey! What can I do for you?"),
("Who are you?", "I am a chatbot."),
("What's your name?", "My name is ChatBot."),
("What do you do?", "I am here to assist you with any questions you might have."),
("How are you?", "I'm fine, thank you."),
("What's going on?", "Nothing much, sir."),
("What's up?", "Just here to help you out. How can I assist you?"),
("Can you help me?", "Of course! What do you need help with?"),
("I need assistance", "Sure, tell me what you need assistance with."),
("What time is it?", "I can't tell time, but you can check your device's clock."),
("What day is it?", "I can't track dates, but your device's calendar can help."),
("Do you like music?", "I don't have preferences, but I can find music recommendations for you!"),
("What's your favorite color?", "I don't have one, but I love helping people with their queries."),
("Goodbye", "Goodbye! Have a great day!"),
("Bye", "See you later!"),
("Thanks", "You're welcome!"),
("Thank you", "No problem! Happy to help."),
("Goodbye", "Goodbye! Have a great day!"),
("Bye", "See you later!"),
("Thanks", "You're welcome!"),
("Thank you", "No problem! Happy to help."),
("Do you like music?", "I don't have preferences, but I can find music recommendations for you!"),
("What's your favorite color?", "I don't have one, but I love helping people with their queries.")
    # Add more conversation pairs as needed
]

def speak(text):
    engine.say(text)
    engine.runAndWait()
def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

        try:
            print("Recognizing...")
            query = recognizer.recognize_google(audio, language='en-us')
            print(f"User said: {query}\n")
        except Exception as e:
            print("Sorry, I couldn't catch that. Can you please repeat?")
            return "None"
        return query.lower()
# Preprocess data
def preprocess(sentence):
    tokens = nltk.word_tokenize(sentence.lower())
    return tokens


# Response generation function
def generate_response(user_input):
    user_input_tokens = preprocess(user_input)
    for pattern, response in conversations:
        pattern_tokens = preprocess(pattern)
        if set(pattern_tokens).intersection(user_input_tokens):
            return response
    return "I'm sorry, I don't understand."

# Main interaction loop
if __name__ == "__main__":
    print("Type 'quit' to exit")
    while True:
        user_input = take_command()
        if user_input.lower() == 'quit':
            break
        response = generate_response(user_input)
        print(f"Bot: {response}")
        speak(response)

