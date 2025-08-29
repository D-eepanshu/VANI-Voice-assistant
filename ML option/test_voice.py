# === IMPORT REQUIRED MODULES ===
import pyttsx3
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import smtplib
import pyautogui
import time
import joblib
import tkinter as tk
from tkinter import messagebox, Scrollbar
import requests
import pyjokes

# === LOAD PRE-TRAINED ML MODEL & VECTORIZER ===
model = joblib.load("ML option/intent_model.pkl")
vectorizer = joblib.load("ML option/vectorizer.pkl")

# === INITIALIZE TEXT-TO-SPEECH ENGINE ===
engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
current_voice_index = 1  # Default to female voice
engine.setProperty('voice', voices[current_voice_index].id)

# === SETUP TKINTER GUI WINDOW ===
root = tk.Tk()
root.title("VANI - Voice Assistant")
root.geometry("550x500")
root.configure(bg="#cde6f5")

# === CREATE TEXT OUTPUT AREA WITH SCROLLBAR ===
frame = tk.Frame(root)
frame.pack(pady=15)

output_text = tk.Text(frame, height=18, width=65, wrap=tk.WORD,
                      font=("Consolas", 11), bg="#ffffff", fg="#222222", bd=2)
output_text.pack(side=tk.LEFT)

scrollbar = Scrollbar(frame, command=output_text.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scrollbar.set)

# === GUI HELPER FUNCTION TO SHOW OUTPUT ===
def display_output(text):
    output_text.insert(tk.END, f"{text}\n")
    output_text.yview(tk.END)

# === SPEAK FUNCTION USING pyttsx3 AND SHOW IN GUI ===
def speak(text):
    display_output(f"Assistant: {text}")
    engine.say(text)
    engine.runAndWait()

# === TAKE USER VOICE COMMAND ===
def takeCommand():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        display_output("🎤 Listening...")
        recognizer.pause_threshold = 1
        audio = recognizer.listen(source)
    try:
        display_output("🧠 Recognizing...")
        query = recognizer.recognize_google(audio, language='en-in')
        display_output(f"User: {query}")
        return query.lower()
    except:
        display_output("❗ Could not recognize speech. Please try again.")
        return "none"

# === PREDICT USER INTENT BASED ON SPOKEN COMMAND ===
def predict_intent(command):
    X_input = vectorizer.transform([command])
    return model.predict(X_input)[0]

# === SEND EMAIL USING SMTP (UPDATE WITH YOUR EMAIL CREDENTIALS) ===
def send_email(to, content):
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login('youremail@gmail.com', 'your-password')  # Replace securely
        server.sendmail('youremail@gmail.com', to, content)
        server.quit()
        return True
    except:
        return False

# === PLAY MUSIC ON YOUTUBE BY SEARCHING AND SIMULATING CLICKS ===
def play_youtube_music(song):
    query = song.replace(' ', '+')
    webbrowser.open(f"https://www.youtube.com/results?search_query={query}")
    speak(f"Searching {song} on YouTube")
    time.sleep(5)
    pyautogui.press('tab', presses=3)
    pyautogui.press('enter')

# === CONTROL YOUTUBE (PAUSE, MUTE, FULL SCREEN, ETC.) ===
def control_youtube(action):
    pyautogui.hotkey('alt', 'tab')  # Switch to YouTube tab
    time.sleep(1)
    controls = {
        'pause': 'space',
        'play': 'space',
        'next': ['shift', 'n'],
        'mute': 'm',
        'unmute': 'm',
        'full screen': 'f'
    }
    key = controls.get(action)
    if isinstance(key, list):
        pyautogui.hotkey(*key)
    elif key:
        pyautogui.press(key)

# === CHANGE ASSISTANT VOICE TO MALE OR FEMALE ===
def change_voice(gender):
    global current_voice_index
    index = 1 if 'female' in gender else 0
    current_voice_index = index
    engine.setProperty('voice', voices[index].id)
    speak(f"Switched to {gender} voice.")

# === FETCH WEATHER USING wttr.in ===
def get_weather():
    speak("Please tell me the city name.")
    city = takeCommand()
    if city == "none": return
    try:
        res = requests.get(f"http://wttr.in/{city}?format=3")
        speak(res.text)
    except:
        speak("Failed to get weather info.")

# === PERFORM BASIC CALCULATION BASED ON USER INPUT ===
def calculate_expression():
    speak("Please state your calculation.")
    expression = takeCommand()
    try:
        result = eval(expression)
        speak(f"The result is {result}")
    except:
        speak("Sorry, I couldn't calculate that.")

# === HANDLE INTENT AND EXECUTE APPROPRIATE ACTION ===
def handle_intent(query):
    intent = predict_intent(query)

    if intent == 'search_wikipedia':
        topic = query.replace("wikipedia", "").strip()
        speak("Searching Wikipedia...")
        try:
            summary = wikipedia.summary(topic, sentences=2)
            speak("According to Wikipedia:")
            speak(summary)
        except:
            speak("Sorry, no result found.")

    elif intent == 'play_music':
        speak("What music should I play?")
        song = takeCommand()
        if song != "none":
            play_youtube_music(song)

    elif intent == 'open_youtube':
        webbrowser.open("https://youtube.com")
        speak("Opening YouTube.")

    elif intent == 'control_youtube':
        actions = ['pause', 'play', 'mute', 'unmute', 'next', 'full screen']
        for act in actions:
            if act in query:
                control_youtube(act)
                speak("Done.")
                return

    elif intent == 'get_time':
        now = datetime.datetime.now().strftime("%H:%M:%S")
        speak(f"The current time is {now}")

    elif intent == 'send_email':
        speak("What should I say?")
        content = takeCommand()
        if content != "none" and send_email("deepanshu@gmail.com", content):
            speak("Email sent successfully.")
        else:
            speak("Failed to send email.")

    elif intent == 'change_voice':
        change_voice(query)

    elif intent == 'exit':
        speak("Goodbye! See you later.")
        root.quit()

    elif intent == 'tell_joke':
        speak(pyjokes.get_joke())

    elif intent == 'get_weather':
        get_weather()

    elif intent == 'calculator':
        calculate_expression()

    else:
        speak("Sorry, I didn’t understand that.")

# === START LISTENING AND PROCESS USER QUERY ===
def start_listening():
    query = takeCommand()
    if query != "none":
        handle_intent(query)

# === GREET USER BASED ON TIME ===
def wish_user():
    hour = datetime.datetime.now().hour
    greeting = "Good Morning" if hour < 12 else "Good Afternoon" if hour < 18 else "Good Evening"
    speak(f"{greeting}! I am your assistant VANI. How may I help you?")

# === GUI BUTTONS FOR INTERACTION ===
listen_button = tk.Button(root, text="🎙️ Start Listening", width=20, bg="#4caf50", fg="white",
                          font=("Arial", 12), command=start_listening)
listen_button.pack(pady=10)

exit_button = tk.Button(root, text="❌ Exit", width=20, bg="#f44336", fg="white",
                        font=("Arial", 12), command=root.quit)
exit_button.pack(pady=10)

# === START APPLICATION ===
wish_user()
root.mainloop()
