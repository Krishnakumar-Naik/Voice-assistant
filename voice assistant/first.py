import sounddevice as sd
import numpy as np
import pyttsx3
import pywhatkit
import wikipedia
import datetime
import os
import pyautogui
import speech_recognition as sr
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import webbrowser
import cv2

# function for camera
def open_camera():
    talk("Opening camera")
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow('Camera', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    cv2.destroyAllWindows()

# Initialize the recognizer and engine
recognizer = sr.Recognizer()
engine = pyttsx3.init()

# Function to make the assistant speak
def talk(text):
    engine.say(text)
    engine.runAndWait()

# Function to capture audio using sounddevice
def capture_audio(duration=5, rate=44100):
    print("Listening...")
    audio_data = sd.rec(int(duration * rate), samplerate=rate, channels=1, dtype='int16')
    print("Listening...")
    sd.wait()  # Wait for the recording to finish
    return audio_data

# Function to recognize speech from audio data
def recognize_speech(audio_data, rate=44100):
    try:
        # Convert audio data to `AudioData` object for SpeechRecognition
        audio = sr.AudioData(audio_data.tobytes(), rate, 2)  # 2 bytes for 'int16'
        command = recognizer.recognize_google(audio).lower()
        print(f"User said: {command}")
        return command
    except sr.UnknownValueError:
        talk("Sorry, I didn't catch that.")
        return ""
    except sr.RequestError as e:
        talk(f"Error with the speech recognition service: {e}")
        return ""

# Function to perform actions
def run_assistant():
    # Show the "Listening..." text
    listening_text.pack(side="bottom", pady=100)

    # Capture audio and recognize speech
    audio_data = capture_audio()
    command = recognize_speech(audio_data)

    # Hide the "Listening..." text after processing
    listening_text.pack_forget()

    # Check for commands
    if 'play' in command:
        song = command.replace('play', '').strip()
        talk(f"Playing {song} on YouTube")
        pywhatkit.playonyt(song)
    
    elif 'time' in command: #tells the time
        current_time = datetime.datetime.now().strftime('%I:%M %p')
        talk(f"The current time is {current_time}")
    
    elif 'search for' in command:#search on the wikipedia 
        query = command.replace('search for', '').strip()
        talk(f"Searching for {query} on Wikipedia")
        try:
            info = wikipedia.summary(query, sentences=2)
            talk(info)
        except wikipedia.DisambiguationError:
            talk("The search term is ambiguous. Please try again.")
        except wikipedia.PageError:
            talk("Sorry, I couldn't find anything on that topic.")

    #open notepad, calculator, linkedin and facebook
    elif 'open' in command:
        app = command.replace('open', '').strip()
        talk(f"Opening {app}")
        if app == 'notepad':
            os.system('notepad')
        elif app == 'calculator':
            os.system('calc')
        elif app == 'linkedin':
            webbrowser.open("https://www.linkedin.com")
        elif app == 'facebook':
            webbrowser.open("https://www.facebook.com")
    
    elif 'search' in command and 'flipkart' in command:
        query = command.replace('search', '').replace('flipkart', '').strip()
        talk(f"Searching for {query} on Flipkart")
        webbrowser.open(f"https://www.flipkart.com/search?q={query}")
    
    elif 'search' in command and 'amazon' in command:
        query = command.replace('search', '').replace('amazon', '').strip()
        talk(f"Searching for {query} on Amazon")
        webbrowser.open(f"https://www.amazon.in/s?k={query}")
    
    elif 'google' in command: #search anything in google
        query = command.replace('google', '').strip()
        talk(f"Searching Google for {query}")
        webbrowser.open(f"https://www.google.com/search?q={query}")
    
    elif 'shutdown' in command: #shoutdown the pc
        talk("Shutting down the system.")
        os.system('shutdown /s /t 1')
    
    elif 'brightness' in command and 'up' in command:
        talk("Increasing brightness")
        pyautogui.hotkey('fn','F8')  # For certain laptops, you might need the 'fn' key
        
    elif 'open camera' in command:
        open_camera() #open camera function call

    elif 'brightness' in command and 'down' in command:
        talk("Decreasing brightness")
        pyautogui.hotkey('fn','F7')  # Same as above
    
    else:
        talk("Sorry, I can't handle that command.") #above commands are not matched
    
    # Update the output window
    output_text.insert(tk.END, f"Assistant: {command}\n")
    output_text.yview(tk.END)

# GUI Setup
def start_listening():
    output_text.insert(tk.END, "Heared\n")
    output_text.yview(tk.END)
    run_assistant()

# Create the main window
root = tk.Tk()
root.title("Voice Assistant")

# Configure window size and layout
root.geometry("1270x720")
root.resizable(False, False)

# Load and resize the background image
bg_image = Image.open("bg2.png")
bg_image = bg_image.resize((1280, 720), Image.Resampling.LANCZOS)
bg_image = ImageTk.PhotoImage(bg_image)

# Create a label to set the image as the background
bg_label = tk.Label(root, image=bg_image)
bg_label.place(relwidth=1, relheight=1)

# Create a frame for the top section
top_frame = tk.Frame(root, bg="#4e4e4e", height=100)
top_frame.pack(fill="x")

# Add title text
title_label = tk.Label(top_frame, text="Voice Assistant", font=("Arial", 24, "bold"), fg="white", bg="#4e4e4e")
title_label.pack(pady=20)

# Create a frame to center the output text
center_frame = tk.Frame(root, bg="black")
center_frame.place(relx=0.5, rely=0.5, anchor="center")

# Create a scrollable text area for output inside the centered frame
output_text = scrolledtext.ScrolledText(center_frame, wrap=tk.WORD, width=100, height=12, font=("Arial", 12), bg="#1e1e1e", fg="white")
output_text.pack(padx=20, pady=20)

# Add a label for "Listening..." text
listening_text = tk.Label(root, text="Listening...", font=("Arial", 16, "bold"), fg="white", bg="black")
listening_text.pack_forget()  # Initially hidden

# Create a 'Start Listening' button
listen_button = tk.Button(root, text="Start Listening", command=start_listening, width=20, height=2, font=("Arial", 14), bg="#4CAF50", fg="white")
listen_button.pack(pady=20)

# Run the GUI
root.mainloop()
