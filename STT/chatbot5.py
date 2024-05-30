import nltk
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import requests
import pyaudio

# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Example conversation pairs
conversations = [
    ("hey Denver", ",Yes sir"),
    ("Hello", "Hello sir!"),
    ("who are you", "I am Denver."),
    ("How are you?", "I'm fine sir, thank you."),
    ("What's your name?", "My name is Denver."),
    ("what's going on", "Nothing much, sir."),
    ("Hi", "Hello! How can I assist you today?"),
    ("Hey", " What can I do for you sir?"),
    ("What do you do?", "I am here to assist you with any questions you might have."),
    ("What's up?", "Just here to help you out. How can I assist you sir?"),
    ("Can you help me?", "Of course! What do you need help with sir?"),
    ("I need assistance", "Sure sir, tell me what you need assistance with."),
    ("What time is it?", "I can't tell time, but you can check your device's clock."),
    ("What day is it?", "I can't track dates, but your device's calendar can help."),
    ("Do you like music?", "I don't have preferences, but I can find music recommendations for you!"),
    ("What's your favorite color?", "I don't have one, but I love helping people with their queries."),
    ("Goodbye", "Goodbye! Have a great day! sir"),
    ("Bye", "See you later! sir"),
    ("Thanks", "You're welcome! sir"),
    ("Thank you", "No problem! Happy to help."),
    ("what are you doing", "Iam just listning for you sir")
]

def speak(text):
    engine.say(text)
    engine.runAndWait()

# def greet():
#     hour = datetime.datetime.now().hour
#     if 0 <= hour < 12:
#         engine.say("Good morning, sir. How can I assist you today?")
#     elif 12 <= hour < 18:
#         engine.say("Good afternoon, sir. How can I assist you today?")
#     else:
#         engine.say(",Good evening, sir. How can I assist you today?")

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

    # Handle specific commands
    if 'wikipedia' in user_input_tokens:
        speak('Searching Wikipedia...')
        query = ' '.join([word for word in user_input_tokens if word != 'wikipedia'])
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        return results

    elif 'open' in user_input_tokens:
        if 'youtube' in user_input_tokens:
            print("sure sir, Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            return "sure sir, Opening YouTube"
        elif 'google' in user_input_tokens:
            print("Opening Google")
            webbrowser.open("https://www.google.com")
            return "Opening Google"

    elif 'play' in user_input:
        if 'music' or 'songs' in user_input_tokens:
            music_dir = 'E:\\music\\hck'  # Change this to your music directory
            if os.path.isdir(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                    return "Playing music"
                else:
                    return "No music files found in the directory."
            else:
                return "Music directory not found."

    elif 'thank' in user_input_tokens or 'see' in user_input_tokens:
        if 'later' in user_input or 'see' in user_input:
            speak(",Goodbye sir. Have a great day!")
            exit()

    # Time API
    if "time" in user_input_tokens:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        return f"The current time is {current_time}. sir "

    # Check for weather-related queries
    if "weather" in user_input_tokens:
        city = None
        if "in" in user_input_tokens:
            in_index = user_input_tokens.index("in")
            if in_index + 1 < len(user_input_tokens):
                city = user_input_tokens[in_index + 1]
        if not city:
            for token in user_input_tokens:
                if token not in ["weather", "in"]:
                    city = token
                    break
        if city:
            return get_weather(city)
        else:
            return "I couldn't determine the city. Please specify the city name."

    # Find the best matching response for general conversations
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
    # hour = datetime.datetime.now().hour
    # # if 0 <= hour < 12:
    #     engine.say("Good morning, sir. How can I assist you today?")
    # elif 12 <= hour < 18:
    #     engine.say("Good afternoon, sir. How can I assist you today?")
    # else:
    #     engine.say(",Good evening, sir. How can I assist you today?")
    # greet()
    while True:
        user_input = take_command()
        if user_input.lower() == 'quit':
            break
        if user_input:
            response = generate_response(user_input)
            print(f"Bot: {response}")
            speak(response)
