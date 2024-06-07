import socket
import speech_recognition as sr
from gtts import gTTS
import os
from enum import Enum

class Start(Enum):
    IDLE = 0
    CHICK = 1
    DINO = 2
    READY = 3

class Movement(Enum):
    DEFEND = 0
    ATTACK1 = 1
    ATTACK2 = 2

HEADER = 64
PORT = 5050
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
# Whatever IP address you found from running ifconfig in terminal.
# SERVER = ""
SERVER = '192.168.0.72'

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
    print(client.recv(2048).decode(FORMAT))

# recognize speech using Google Speech Recognition 
character = Start.IDLE.value
while(1):
    start = input("say start: ")
    if start == "start":
        character = Start.CHICK.value
        send(Start.CHICK.value)
        break
while(1):
    ready = input("say ready or pick character (1) chick (2) dino: ")
    if ready == "chicken":
        character = Start.CHICK.value
        send(Start.CHICK.value)
    elif ready == "dinosaur":
        character = Start.DINO.value
        send(Start.DINO.value)
    if ready == "ready":          
        send(Start.READY.value)
        break
if character == Start.CHICK.value: 
    while(1):
        movement = (input("(1) defend, (2) throw, (3) hit"))
        if movement == "defend":
            send(f"{Movement.DEFEND.value}")
        elif movement == "throw":
            send(f"{Movement.ATTACK1.value}")
        elif movement == "hit":
            send(f"{Movement.ATTACK2.value}")

if character == Start.DINO.value: # Dino
    while(1):
        movement = (input("(1) defend, (2) fire, (3) scratch"))
        if movement == "defend":
            send(f"{Movement.DEFEND.value}")
        elif movement == "fire":
            send(f"{Movement.ATTACK1.value}")
        elif movement == "scratch":
            send(f"{Movement.ATTACK2.value}")

send(DISCONNECT_MESSAGE)