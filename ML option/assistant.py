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
    print("Assistant:", audio)
    engine.say(audio)
    engine.runAndWait()

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)
    try:
        print("🧠 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"🗣️ User said: {query}\n")
    except Exception:
        print("❗ Please say that again...")
        return "None"
    return query

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.ehlo()
    server.starttls()
    server.login('youremail@gmail.com', 'your-password')  # Replace!
    server.sendmail('youremail@gmail.com', to, content)
    server.close()

def playYouTubeMusic(song_name):
    query = song_name.replace(' ', '+')
    url = f"https://www.youtube.com/results?search_query={query}"
    webbrowser.open(url)
    speak(f"Searching {song_name} on YouTube")
    time.sleep(5)  # wait for page to load
    pyautogui.press('tab', presses=3)
    pyautogui.press('enter')

def controlYouTube(action):
    # Bring YouTube window into focus
    pyautogui.hotkey('alt', 'tab')  # Alt+Tab to switch to the browser window
    time.sleep(1)  # wait for the browser to be in focus

    if action in ['pause', 'play']:
        pyautogui.press('space')  # Play/Pause key
    elif action == 'next':
        pyautogui.hotkey('shift', 'n')  # Next video key
    elif action == 'full screen':
        pyautogui.press('f')  # Full screen key
    elif action in ['mute', 'unmute']:
        pyautogui.press('m')  # Mute/Unmute key

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
root.title("Voice Assistant")
root.geometry("400x400")
root.config(bg="lightblue")

# Textbox to display assistant's responses
output_text = tk.Text(root, height=10, width=40, wrap=tk.WORD)
output_text.pack(pady=10)

# Function to display output in the text box
def display_output(text):
    output_text.insert(tk.END, f"Assistant: {text}\n")
    output_text.yview(tk.END)

# Move the window to create a dynamic effect
def move_window():
    current_pos = root.winfo_x(), root.winfo_y()
    new_x = current_pos[0] + 1
    if new_x > 600:  # Reset the position to start again when it goes off the screen
        new_x = 0
    root.geometry(f"400x400+{new_x}+{current_pos[1]}")
    root.after(10, move_window)  # Repeat the function every 10 ms

# Greet user
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if 0 <= hour < 12:
        speak("Good Morning!")
    elif 12 <= hour < 18:
        speak("Good Afternoon!")
    else:
        speak("Good Evening!")
    speak("I am your assistant. Please tell me how may I help you.")

def startListening():
    query = takeCommand().lower()
    if query == "none":
        return
    intent = predict_intent(query)
    
    display_output(f"User: {query}")

    if intent == 'search_wikipedia':
        display_output("Searching Wikipedia...")
        speak('Searching Wikipedia...')
        try:
            topic = query.replace("wikipedia", "").strip()
            results = wikipedia.summary(topic, sentences=2)
            display_output(results)
            speak("According to Wikipedia")
            speak(results)
        except Exception:
            speak("Sorry, I couldn't find anything on Wikipedia.")
    
    elif intent == 'play_music':
        display_output("What music would you like to play?")
        speak("What music would you like to play?")
        song = takeCommand()
        playYouTubeMusic(song)
    
    elif intent == 'open_youtube':
        display_output("Opening YouTube")
        speak("Opening YouTube")
        webbrowser.open("https://www.youtube.com")
    
    elif intent == 'control_youtube':
        display_output("Executing YouTube control.")
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
            to = "deepanshu@gmail.com"  # Replace with real email
            sendEmail(to, content)
            display_output("Email has been sent.")
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
        display_output("Sorry, I didn't understand that.")

# Button for listening
listen_button = tk.Button(root, text="Start Listening", width=20, command=startListening)
listen_button.pack(pady=10)

# Button to exit the application
exit_button = tk.Button(root, text="Exit", width=20, command=root.quit)
exit_button.pack(pady=10)

# Run the GUI 
wishMe()
move_window()  # Start the moving window effect
root.mainloop()
