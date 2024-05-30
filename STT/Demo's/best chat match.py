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
import datetime
import requests
# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Example conversation pairs
conversations = [
    ("Hello", "Hi there!"),
    ("who are you", "I am Denver."),
    ("How are you?", "I'm fine, thank you."),
    ("What's your name?", "My name is Denver."),
    ("what's going on", "Nothing much, sir."),
    ("who are you", "I am Denver."),
    ("Hi", "Hello! How can I assist you today?"),
    ("Hey", "Hey! What can I do for you?"),
    ("What do you do?", "I am here to assist you with any questions you might have."),
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

# Jaccard similarity function
def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    return intersection / union
def get_weather(city):
    base_url = f"http://wttr.in/{city}?format=3"
    response = requests.get(base_url)
    if response.status_code == 200:
        return response.text
    else:
        return "I couldn't retrieve the weather information right now. Please try again later."

# Response generation function
def generate_response(user_input):
    user_input_tokens = preprocess(user_input)
    if 'wikipedia' in user_input_tokens:
        speak('Searching Wikipedia...')
        query = user_input_tokens.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in user_input_tokens:
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in user_input_tokens:
        webbrowser.open("https://www.google.com")
    elif 'play music' in user_input_tokens:
        music_dir = 'E:\\music\\hck'  # Change this to your music directory
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
    elif 'the time' in user_input_tokens:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif 'exit' in user_input_tokens:
        speak("Goodbye, sir. Have a great day!")
        exit()
    #timeapi
    if "time" in user_input_tokens:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}."
    # Check for weather-related queries
    if "weather" in user_input_tokens:
        # Extract the city name from the user input
        for token in user_input_tokens:
            if token != "weather":
                city = token
                break
        return get_weather("coimbatore")
    max_similarity = 0
    best_response = "I'm sorry, I don't understand."

    for pattern, response in conversations:
        pattern_tokens = preprocess(pattern)
        similarity = jaccard_similarity(set(user_input_tokens), set(pattern_tokens))
        if similarity > max_similarity:
            max_similarity = similarity
            best_response = response

    return best_response

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
