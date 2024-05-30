import pyaudio
import os
from pocketsphinx import LiveSpeech

# Set up PyAudio
p = pyaudio.PyAudio()
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024

# Create a generator for live speech recognition
def recognize_speech():
    speech = LiveSpeech(
        verbose=False,
        sampling_rate=RATE,
        buffer_size=CHUNK
    )
    for phrase in speech:
        yield str(phrase)

# Main function
def main():
    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print("Listening...")

    try:
        for phrase in recognize_speech():
            print("You said:", phrase)
    except KeyboardInterrupt:
        print("Stopped listening.")
        stream.stop_stream()
        stream.close()
        p.terminate()

if __name__ == "__main__":
    main()