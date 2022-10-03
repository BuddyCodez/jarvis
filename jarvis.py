import requests
import pyttsx3
import time
import speech_recognition as sr
import pyautogui
from AppOpener import run
from datetime import datetime
now = datetime.now()
r, mic = sr.Recognizer(), sr.Microphone()

welcome = "Good Morning Sir"
if (now.hour > 12):
    welcome = "Good Afternoon Sir"
if (now.hour > 17):
    welcome = "Good Evening Sir"

# callback fuction :
def callback(recognizer, audio, text=""):
    try:
        text = recognizer.recognize_google(audio, language="en-IN")
    except:
        pass
    if (not text):
        return
    print("Your Command: ", text)
    if (text.startswith("open")):
        cmd = text.split("open")[1]
        print(cmd)
        pyttsx3.speak("Opening ..." + cmd)
        run(cmd)
    elif (text.startswith("play")):
        pyttsx3.speak(f"Playing {text.split('play')[1]} ....")
        run("spotify")
        time.sleep(5)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(2)
        pyautogui.write(text.split("play")[1], interval=0.1)
        time.sleep(2)
        for key in ['enter', 'tab', 'enter', 'enter']:
            time.sleep(1)
            pyautogui.press(key)
    else:
        response = requests.get(
            "http://api.brainshop.ai/get?bid=169326&key=jdvXg0wzF22z63Q8&uid=JarvisBot&msg=" + text)
        print("Jarvis: ", response.json()["cnt"])
        pyttsx3.speak(response.json()["cnt"])


with mic as source:
    start_msg = welcome + ", I am Jarvis, Your Personal Assistant. How May I help you?"
    print(start_msg)
    pyttsx3.speak(start_msg)
    r.adjust_for_ambient_noise(source)
    r.pause_threshold = 0.5
r.listen_in_background(mic, callback)

while True:
    time.sleep(2)
