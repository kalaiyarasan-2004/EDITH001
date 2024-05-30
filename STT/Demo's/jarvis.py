import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import webbrowser
import os
import pyaudio

# Initialize speech recognition and text-to-speech engines
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to convert text to speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to greet user
def greet():
    hour = datetime.datetime.now().hour
    if 0 <= hour < 12:
        speak("Good morning, sir. How can I assist you today?")
    elif 12 <= hour < 18:
        speak("Good afternoon, sir. How can I assist you today?")
    else:
        speak(",Good evening, sir. How can I assist you today?")
        # speak(", sir, iam ready")

# Function to take user command via voice
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

# Function to perform various tasks based on user command
def execute_command(query):
    if 'wikipedia' in query:
        speak('Searching Wikipedia...')
        query = query.replace("wikipedia", "")
        results = wikipedia.summary(query, sentences=2)
        speak("According to Wikipedia")
        print(results)
        speak(results)
    elif 'open youtube' in query:
        webbrowser.open("https://www.youtube.com")
    elif 'open google' in query:
        webbrowser.open("https://www.google.com")
    elif 'play music' in query:
        music_dir = 'E:\\music\\hck'  # Change this to your music directory
        songs = os.listdir(music_dir)
        os.startfile(os.path.join(music_dir, songs[0]))
    elif 'the time' in query:
        current_time = datetime.datetime.now().strftime("%H:%M")
        speak(f"The current time is {current_time}")
    elif 'exit' in query:
        speak("Goodbye, sir. Have a great day!")
        exit()
    # elif 'scan' or 'ip' in query:


# Main function to control the flow of the program
def main():
    greet()
    while True:
        query = take_command()
        execute_command(query)

if __name__ == "__main__":
    main()
