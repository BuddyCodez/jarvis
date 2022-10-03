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

event = "Good Morning Sir"
if (now.hour > 12):
    event = "Good Afternoon Sir"
if (now.hour > 17):
    event = "Good Evening Sir"

listener = sr.Recognizer()
speaker = pyttsx3.init()
listener.pause_threshold = 0.5
listener.energy_threshold = 300


def speak(text):
    print(text)
    speaker.say(text)
    speaker.runAndWait()


speak(event)
speak("I am Jarvis, How can I help you ?")


def take_command():
    try:
        with sr.Microphone() as source:
            print("Listening to your Commands ...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            print(command)
            return command
    except:
        return None


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}





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
        complete_url = base_url + "appid=" + api_key + "&q=" + city 
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            print(x)
            y = x["main"]
            current_temperature = y["temp"]
            current_pressure = y["pressure"]
            current_humidity = y["humidity"]
            z = x["weather"]
            weather_description = z[0]["description"]
            speak(f"Temperature in {city} is {str(current_temperature)} Kelvin")
            speak(f"Atmospheric Pressure in {city} is {str(current_pressure)}")
            speak(f"Humidity in {city} is {str(current_humidity)}")
            speak(str(weather_description))

    elif len(text) > 3:
        response = requests.get(
            "http://api.brainshop.ai/get?bid=169326&key=jdvXg0wzF22z63Q8&uid=JarvisBot&msg=" + text)
        speak(response.json()["cnt"])
    else:
        speak("please Say it Again ..")


while True:
    callback()
