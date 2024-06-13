import socket
import speech_recognition as sr
from gtts import gTTS
import os
from enum import Enum

class Start(Enum):
    START = 0
    CHICK = 1
    DINO = 2
    READY = 3

class Movement(Enum):
    DEFEND = 4
    ATTACK1 = 5
    ATTACK2 = 6

HEADER = 64
PORT = 5055
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# Whatever IP address you found from running ifconfig in terminal.
# SERVER = ""
SERVER = '192.168.0.73'

ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Officially connecting to the server.
client.connect(ADDR)

def send(msg):
    strmsg = str(msg)
    message = strmsg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' * (HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    

def get_audio_with_minimum_volume(min_value=125):
    with sr.Microphone() as source:
        print("Please wait. Calibrating microphone...")
        r.adjust_for_ambient_noise(source, duration=1)
        
        print("Waiting for loud enough sound...")
        
        while True:
            # Listen for a short duration to capture background noise
            audio = r.listen(source, phrase_time_limit=1)
            # Get the volume level
            volume = audio.frame_data
            # Calculate average volume level
            average_volume = sum(audio.frame_data) / len(audio.frame_data)
            
            print(f"Current volume level: {average_volume}")
            
            # If the volume level is greater than the threshold, break the loop
            if average_volume > min_value:
                print("Loud enough sound detected!")
                return audio
#obtain audio from the microphone
r=sr.Recognizer() 


# recognize speech using Google Speech Recognition 
speak = ""
character = Start.CHICK.value
while(1):
    print("Google Speech Recognition thinks you said:");
    try:
        audio = get_audio_with_minimum_volume()
        speak = r.recognize_google(audio)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("No response from Google Speech Recognition service: {0}".format(e))
        print(speak);
    if speak == "start":
        send(Start.START.value)
        break
while(1):
    print("Google Speech Recognition thinks you said:");
    try:
        audio = get_audio_with_minimum_volume()
        speak = r.recognize_google(audio)
        if isinstance(speak, dict):
            print("ojj\nojj\nojj\nojj\n\n\n\n\n")
            speak = speak["alternative"][0]["transcript"]
        if speak == "chicken":
            character = Start.CHICK.value
            send(Start.CHICK.value)
        elif speak == "dinosaur":
            character = Start.DINO.value
            send(Start.DINO.value)
        if speak == "ready":
            send(Start.READY.value)
            break
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("No response from Google Speech Recognition service: {0}".format(e))
if character == Start.CHICK.value: 
    while(1):
        #receive stop
        print("Google Speech Recognition thinks you said:")
        try:
            audio = get_audio_with_minimum_volume()
            speak = r.recognize_google(audio)
            if speak == "defend":
                send(f"{Movement.DEFEND.value}")
            elif speak == "throw":
                send(f"{Movement.ATTACK1.value}")
            elif speak == "hit":
                send(f"{Movement.ATTACK2.value}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("No response from Google Speech Recognition service: {0}".format(e))

if character == Start.DINO.value: # Dino
    while(1):
        #receive stop
        print("Google Speech Recognition thinks you said:")
        try:
            audio = get_audio_with_minimum_volume()
            speak = r.recognize_google(audio)
            if speak == "defend":
                send(f"{Movement.DEFEND.value}")
            elif speak == "fire":
                send(f"{Movement.ATTACK1.value}")
            elif speak == "scratch":
                send(f"{Movement.ATTACK2.value}")
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
        except sr.RequestError as e:
            print("No response from Google Speech Recognition service: {0}".format(e))

send(DISCONNECT_MESSAGE)
