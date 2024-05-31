import nltk
import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import requests
import pyaudio
import stdlibWithroll
import oneprint
import pywhatkit
import pyautogui
# Initialize recognizer and text-to-speech engine
recognizer = sr.Recognizer()
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
engine.setProperty('voices',voices[0].id)
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        engine.say("Good morning, sir. How can I assist you today?")
    elif 12 <= hour < 18:
        engine.say("Good afternoon, sir. How can I assist you today?")
    else:
        engine.say(",Good evening, sir. How can I assist you today?")

# Example conversation pairs
conversations = [
    ("hey Denver", ",Yes sir"),
    ("Hello", "Hello sir!"),
    ("How are you?", "I'm fine sir,"),
    ("What's your name?", "iam is Denver."),
    ("what's going on", "Nothing much, sir."),
    ("help me?", "Of course! What do you need help with sir?"),
    ("Do you like music?", "I don't have preferences, but I can find music recommendations for you!"),
    ("Goodbye", "Goodbye! Have a great day! sir"),
    ("Thanks", "You're welcome! sir"),
    ("Thank you", "No problem! Happy to help."),
    ("what are you doing", "Iam just listning for you sir")
]

def speak(text):
    engine.say(text)
    engine.runAndWait()



def take_command():
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold=1
        recognizer.adjust_for_ambient_noise(source,duration=1)
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        query = recognizer.recognize_google(audio, language='en-us')
        print(f"User said: {query}\n")
    except Exception as e:
        print(e)
        speak("")
        query = "None"
    return query.lower()
def wakeup():
    recognizer=sr.Recognizer()
    with sr.Microphone() as source:
        print("Denver is Sleeping...")
        recognizer.pause_threshold=1
        recognizer.adjust_for_ambient_noise(source,duration=1)
        audio = recognizer.listen(source)
    try:
        query=recognizer.recognize_google(audio,language='en-us')
        print(f"User said: {query}\n")
    except Exception as e:
           query = ""
    return query.lower()
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning, sir. How can I assist you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir. How can I assist you today?")
    else:
        speak(",Good evening, sir. How can I assist you today?")
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


    if 'open' in user_input_tokens:
        if 'youtube' in user_input_tokens:
            print("sure sir, Opening YouTube")
            webbrowser.open("https://www.youtube.com")
            return "sure sir, Opening YouTube"
        elif 'google' in user_input_tokens:
            print("Opening Google")
            webbrowser.open("https://www.google.com")
            return "Opening Google"

    elif 'play' in user_input:
        if 'local' or '' in user_input_tokens:
            music_dir = 'E:\\music\\hck'  # Change this to your music directory
            if os.path.isdir(music_dir):
                songs = os.listdir(music_dir)
                if songs:
                    os.startfile(os.path.join(music_dir, songs[0]))
                    speak("Playing music")
                    return 0
                else:
                    return "No music files found in the directory."
            else:
                return "Music directory not found."
        elif 'play' in user_input_tokens:
            user_input=user_input.replace('play','')
            speak("playing"+user_input)
            pywhatkit.playonyt(user_input)
        

    elif 'thank' in user_input_tokens or 'see' in user_input_tokens:
        if 'later' in user_input or 'see' in user_input:
            speak(",Goodbye sir. Have a great day!")
            exit()
    elif 'scan' in user_input_tokens:
        if 'face' in user_input:
            speak("Sure sir")
            oneprint.facerec()
    elif 'find' in user_input_tokens:
        if 'someone' in user_input or 'find someone' in user_input:
            try:
                speak("Sure sir, tell a name")
                student_name = take_command()
                stdlibWithroll.main(student_name)
            except:
                speak("sorry sir")
    elif 'type' in user_input_tokens:
        user_input=user_input.replace('type','')
        speak("writting")
        pyautogui.write(user_input)
    elif 'who' in user_input_tokens:
        speak('')
        try:
            query = user_input.replace("who","") and user_input.replace("is","") and user_input.replace("denver","")
            
            results = wikipedia.summary(query, sentences=1)
            speak("According to Wikipedia")
            return results
        except:
            print("no result")
            speak("No results found")

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
    best_response = ""

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
    
    while True:
        user_input=wakeup().lower()
        if "wake up" in user_input or "wakeup" in user_input:
            greet()
            while True:
                user_input = take_command()
                if user_input.lower() == 'exit':
                    break
                if user_input:
                    response = generate_response(user_input)
                    print(f"Bot: {response}")
                    speak(response)
                if "Sleep" in user_input:
                    speak("iam muting sir")
                    break