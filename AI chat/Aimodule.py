import os
import wave
import json
import vosk
import pyaudio

# Function to recognize speech
def listen():
    model_path = "E:\\vosk-model-en-us-0.22"
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}. Please download it.")
        return ""

    vosk.SetLogLevel(0)
    model = vosk.Model(model_path)
    recognizer = vosk.KaldiRecognizer(model, 16000)
    
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)
    stream.start_stream()
    
    print("Listening...")
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data):
            result = recognizer.Result()
            result_json = json.loads(result)
            return result_json['text']
        elif recognizer.PartialResult():
            result_partial = recognizer.PartialResult()
            print(result_partial)

# Example usage
print(listen())
