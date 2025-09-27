# assistant.py
import speech_recognition as sr
import pyttsx3
import wikipedia
import webbrowser
import requests
import time
import sys
from datetime import datetime

# Initialize
engine = pyttsx3.init()
r = sr.Recognizer()
WAKE_WORD = "assistant"   # say "assistant" before commands (simple wake-word)

def speak(text):
    print("Assistant:", text)
    engine.say(text)
    engine.runAndWait()

def listen(timeout=5, phrase_time_limit=6):
    with sr.Microphone() as mic:
        r.adjust_for_ambient_noise(mic, duration=0.5)
        try:
            audio = r.listen(mic, timeout=timeout, phrase_time_limit=phrase_time_limit)
            return r.recognize_google(audio)
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            speak("Speech recognition service unreachable.")
            return ""

def handle_command(text):
    text = text.lower()
    # simple commands
    if "time" in text:
        speak("The time is " + datetime.now().strftime("%I:%M %p"))
    elif "date" in text:
        speak("Today is " + datetime.now().strftime("%A, %B %d, %Y"))
    elif text.startswith("search wikipedia for") or "wikipedia" in text:
        # parse topic
        topic = text.replace("search wikipedia for", "").replace("wikipedia", "").strip()
        if not topic:
            speak("What should I search for on Wikipedia?")
            topic = listen()
        if topic:
            speak(f"Searching Wikipedia for {topic}")
            try:
                summary = wikipedia.summary(topic, sentences=2)
                speak(summary)
            except Exception as e:
                speak("Couldn't get Wikipedia result.")
    elif "open youtube" in text or "youtube" in text:
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    elif "weather in" in text:
        # simple public API-free example using wttr.in
        city = text.split("weather in")[-1].strip()
        if not city:
            speak("Which city?")
            city = listen()
        if city:
            try:
                url = f"http://wttr.in/{city}?format=3"
                r = requests.get(url)
                speak(r.text)
            except Exception:
                speak("Couldn't fetch weather.")
    elif "stop" in text or "exit" in text or "quit" in text:
        speak("Goodbye!")
        sys.exit(0)
    else:
        speak("I did not understand. You can say: time, date, search wikipedia for..., weather in..., open youtube, or stop.")

def main_loop():
    speak("Ready. Say 'assistant' followed by a command.")
    while True:
        text = listen(timeout=6, phrase_time_limit=5)
        if not text:
            continue
        print("Heard:", text)
        # simple wake-word detection
        if WAKE_WORD in text.lower():
            # capture the remainder of what user said after wake word
            after = text.lower().split(WAKE_WORD, 1)[-1].strip()
            if not after:
                speak("Yes?")
                after = listen(timeout=5, phrase_time_limit=6)
            if after:
                handle_command(after)
        else:
            # optional: react to single-shot commands without wake-word
            # Uncomment to allow direct commands:
            # handle_command(text)
            pass

if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        speak("Shutting down.")
