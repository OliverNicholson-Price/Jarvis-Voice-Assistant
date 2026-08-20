import time
import pyttsx3
import simple_webbrowser
import speech_recognition as sr
from pydub import AudioSegment
from pydub.playback import play
import random
from obsws_python import ReqClient

r = sr.Recognizer()
command = ""
responses = ["Yes sir.", "Of course sir.", "Understood sir.", "On it sir.", "Right away sir."]
while True:
    print("Would you like to enable OBS commands? Enter 1 for yes or 2 for no.")
    choice = input()
    try:
        choice = int(choice)
    except ValueError:
        choice = 0
    if choice == 1:
        serverPassword = input("Please enter your OBS WebSocket Server password: ")
        try:
         obs = ReqClient(
            host="localhost",
            port=4455,
            password=serverPassword
         )
         obs.start_replay_buffer()
         obsEnable = True
         break
        except:
            print("OBS Server password is incorrect, disabling OBS commands.")
            obsEnable = False
            break
    elif choice == 2:
        print("Disabling OBS commands.")
        obsEnable = False
        break
    else:
        print("Please enter a valid option.")

def speak(speech):
    engine = pyttsx3.init()
    engine.say(speech)
    engine.runAndWait()
    engine.stop()


def listen():
    with sr.Microphone() as source:
        audio_text = r.listen(source)
        try:
            speech = r.recognize_google(audio_text).lower()
            print("Text: " + speech)
            return speech
        except:
            return ""


speak("JARVIS online. How can I help you?")
while True:
    while command == "":
        command = listen()
    if "shut down" in command or "power off" in command or "shutdown" in command:
        speak(random.choice(responses))
        speak("Shutting down. Have a good day.")
        obs.stop_replay_buffer()
        break
    elif "what" in command and "time" in command:
         speak(random.choice(responses))
         out = str(time.ctime())
         speak("It is currently" + out)
         command = ""
    elif "repeat" in command and "say" in command:
         speak(random.choice(responses))
         speak("What should I say?")
         while True:
            text = str(listen())
            if text != "" :
               speak(text)
               break
            else:
               speak("Sorry, I didn't catch that, please try again.")
         text = str(listen())
         speak(text)
         command = ""
    elif "open website" in command:
         speak(random.choice(responses))
         speak("What website should I open?")
         while True:
            site = str(listen())
            if site != "" :
               simple_webbrowser.website(site)
               break
            else:
               speak("Sorry, I didn't catch that, please try again.")
         command = ""
    elif "open" in command and "weather" in command:
        speak(random.choice(responses))
        simple_webbrowser.website("https://www.google.com/search?q=weather")
        command = ""
    elif "clip that" in command and obsEnable == True:
        obs.save_replay_buffer()
        speak(random.choice(responses))
        command = ""
    elif "open" in command and "music" in command:
        speak(random.choice(responses))
        simple_webbrowser.website("https://open.spotify.com")
        command = ""
    else:
        command = ""
