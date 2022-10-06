import sys
import webbrowser
import speech_recognition as sr
import pyttsx3, json
from AppOpener import run
import requests
import pywhatkit
from datetime import datetime
now = datetime.now()
# ! Weather Api
api_key = "915f78753ce8e2e84a94d0e3f79a269b"
base_url = "http://api.openweathermap.org/data/2.5/weather?"



listener = sr.Recognizer()
speaker = pyttsx3.init()
listener.pause_threshold = 1


def speak(text):
    print(text)
    speaker.say(text)
    speaker.runAndWait()


def wish():
    event = "Good Morning Sir"
    if (now.hour > 12):
        event = "Good Afternoon Sir"
    if (now.hour > 17):
        event = "Good Evening Sir"
    speak(event)
    speak("I am Jarvis a Personal Assistant, How may I help you ?")


def Recognize(audio):
    try:
        print("Recognizing ...")
        text = listener.recognize_google(audio)
        return text
    except:
        return None
def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening to your Commands ...")
            listener.adjust_for_ambient_noise(source)

            voice = listener.listen(source, timeout=4, phrase_time_limit=7)
            command = Recognize(voice)
            command = command.lower()
            print(command)
            return command
    except:
        return None


wish()
def callback():
    text = take_command()
    if (not text):
        print('No Command is given')
        return callback()
    if 'open' in text:
        cmd = text.split("open")[1]
        print(cmd)
        speak("Opening ..." + cmd)
        try:
            run(cmd)
        except:
            print("Sorry, I can't open this app, Trying to open it on the web")
    elif 'web' in text:
        cmd = text.split("web")[1]
        webbrowser.open(cmd)
        speak(f"Opening .... {cmd}")     
    elif 'play' in text:
        song = text.replace('play', '')
        pyttsx3.speak(f"Playing {song} ....")
        pywhatkit.playonyt(song)
    elif 'time' in text:
        current_time = datetime.now().strftime('%I:%M %p')
        print(current_time)
        speak(f"current time is {current_time}")
    elif 'temperature in' in text:
        city = text.split("in")[1]  # ! Logic to get city name
        complete_url = base_url + "&units=metric&appid=" + api_key + "&q=" + city
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            print(x)
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            visiblity = x["visibility"]
            z = x["weather"]
            weather_description = z[0]["description"]
            speak(f"Temperature in {city} is {str(current_temperature)} Celcius")
            speak(
                f"Atmospheric Pressure in {city} is {str(current_pressure)} Hectopascal")
            speak(f"Humidity in {city} is {str(current_humidity)} percentage")
            speak(f"Visiblity in {city} is {visiblity / 1000} km")
            speak("Its seems like " + str(weather_description))
    elif 'switch off' in text or 'turn off' in text or 'shutdown' in text:
        speak('Going for a sleep sir.')
        sys.exit()
    elif len(text) > 3:
        response = requests.get(
            "http://api.brainshop.ai/get?bid=169326&key=jdvXg0wzF22z63Q8&uid=JarvisBot&msg=" + text)
        speak(response.json()["cnt"])
    else:
        speak("please Say it Again ..")


while True:
    callback()
