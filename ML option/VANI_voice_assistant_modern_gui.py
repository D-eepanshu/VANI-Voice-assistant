import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import random
import pyautogui
import time
import joblib
import tkinter as tk
from tkinter import messagebox

# Load ML model and vectorizer
model = joblib.load("ML option/intent_model.pkl")
vectorizer = joblib.load("ML option/vectorizer.pkl")

# Initialize TTS engine
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
current_voice_index = 1
engine.setProperty('voice', voices[current_voice_index].id)

# Helper functions
def speak(audio):
    output_text.insert(tk.END, f"Assistant: {audio}\n")
    output_text.yview(tk.END)
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone(device_index=3) as source:  # Updated microphone index
        speak("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        speak("Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        output_text.insert(tk.END, f"User: {query}\n")
        return query
    except Exception:
        speak("Say that again please...")
        return "None"

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('youremail@gmail.com', 'your-password') 
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def playYouTubeMusic(song_name):
    query = song_name.replace(' ', '+')
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    speak(f"Searching {song_name} on YouTube")
    time.sleep(5)
    pyautogui.press('tab', presses=3)
    pyautogui.press('enter')

def controlYouTube(action):
    pyautogui.hotkey('alt', 'tab')
    time.sleep(1)
    if action in ['pause', 'play']:
        pyautogui.press('space')
    elif action == 'next':
        pyautogui.hotkey('shift', 'n')
    elif action == 'full screen':
        pyautogui.press('f')
    elif action in ['mute', 'unmute']:
        pyautogui.press('m')

def changeVoice(gender):
    global current_voice_index
    if 'female' in gender:
        current_voice_index = 1
        engine.setProperty('voice', voices[1].id)
        speak("Switched to female voice.")
    elif 'male' in gender:
        current_voice_index = 0
        engine.setProperty('voice', voices[0].id)
        speak("Switched to male voice.")
    else:
        speak("Sorry, I can only switch between male and female voices.")

def predict_intent(command):
    X_input = vectorizer.transform([command])
    return model.predict(X_input)[0]

# GUI Setup
root = tk.Tk()
root.title("VANI - Voice Assistant")
root.geometry("500x600")
root.config(bg="#1f1f2e")

# Header
header = tk.Label(root, text="VANI - Your Voice Assistant", font=("Helvetica", 18, "bold"), bg="#1f1f2e", fg="cyan")
header.pack(pady=20)

# Output box
output_text = tk.Text(root, height=15, width=55, wrap=tk.WORD, bg="#2c2c3c", fg="white", font=("Consolas", 10))
output_text.pack(pady=10)

# Function to start voice recognition
def startListening():
    query = takeCommand().lower()
    if query == "none":
        return
    intent = predict_intent(query)

    if intent == 'search_wikipedia':
        speak('Searching Wikipedia...')
        try:
            topic = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(topic, sentences=2)
            speak("According to Wikipedia")
            speak(results)
        except Exception:
            speak("Sorry, I couldn't find anything on Wikipedia.")

    elif intent == 'play_music':
        speak("What music would you like to play?")
        song = takeCommand()
        playYouTubeMusic(song)

    elif intent == 'open_youtube':
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")

    elif intent == 'control_youtube':
        if 'pause' in query or 'play' in query:
            controlYouTube('pause')
        elif 'mute' in query:
            controlYouTube('mute')
        elif 'unmute' in query:
            controlYouTube('unmute')
        elif 'next' in query:
            controlYouTube('next')
        elif 'full screen' in query:
            controlYouTube('full screen')
        speak("Executed YouTube control.")

    elif intent == 'get_time':
        strTime = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The time is {strTime}")

    elif intent == 'send_email':
        try:
            speak("What should I say?")
            content = takeCommand()
            to = "deepanshu@gmail.com"  # Update with actual recipient
            sendEmail(to, content)
            speak("Email has been sent.")
        except Exception as e:
            print(e)
            speak("Sorry, I couldn't send the email.")

    elif intent == 'change_voice':
        if 'female' in query:
            changeVoice('female')
        elif 'male' in query:
            changeVoice('male')
        else:
            speak("Please specify male or female voice.")

    elif intent == 'exit':
        speak("Goodbye Sir!")
        root.quit()

    else:
        speak("Sorry, I didn't understand that.")

# Buttons
listen_button = tk.Button(root, text="🎤 Start Listening", font=("Helvetica", 12), bg="cyan", fg="black", command=startListening)
listen_button.pack(pady=20)

exit_button = tk.Button(root, text="❌ Exit", font=("Helvetica", 12), bg="red", fg="white", command=root.quit)
exit_button.pack(pady=10)

# Greeting
hour = int(datetime.datetime.now().hour)
if 0 <= hour < 12:
    greet = "Good Morning!"
elif 12 <= hour < 18:
    greet = "Good Afternoon!"
else:
    greet = "Good Evening!"
speak(greet)
speak("I am VANI, your assistant. Please tell me how may I help you.")

root.mainloop()
# This code implements a modern GUI for a voice assistant named VANI using Python's Tkinter and speech recognition libraries.
# It includes functionalities like searching Wikipedia, playing music on YouTube, controlling YouTube playback,
# sending emails, changing voice, and more. The assistant uses a machine learning model to predict user intents based on voice commands.
# The GUI is designed to be user-friendly with buttons for interaction