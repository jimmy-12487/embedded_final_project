import sys

import pygame
from pygame.locals import *

import Characters.characters as characters
from Scene.say_start import say_start_scene
from Scene.ready import ready_scene
from Scene.playing import playing_scene
from enums import *
    
import threading
import socket

HEADER = 64
PORT = 5050
SERVER = '192.168.0.72'
ADDR = (SERVER, PORT)
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
BACKGROUND_COLOR = (255, 255, 255)
ROLE_NUMBER = 2

class MainGame():
    def __init__(self, WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR, caption=None):
        pygame.init()
        
        self.surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.main_clock = pygame.time.Clock()
        '''
            set up scenes
        '''
        self.scenes = [say_start_scene(), ready_scene()]
        
        
        self.game_state = GAME_STATE.SAY_START
        self.current_scene = self.scenes[self.game_state]
        
        self.surface.fill(BACKGROUND_COLOR)
        self.user_input = {}
    
    def __create_role(self, p):
        if p[0] == 0:
            if p[1] == True:
                return characters.Chicken(WINDOW_WIDTH, WINDOW_HEIGHT, (100, WINDOW_HEIGHT - 412), (80, 0), (0, 0), p[1])    
            else:
                return characters.Chicken(WINDOW_WIDTH, WINDOW_HEIGHT, (660, WINDOW_HEIGHT - 412), (630, 0), (1052, 0), p[1])    
        elif p[0] == 1:
            if p[1] == True:
                return characters.Dinosaur(WINDOW_WIDTH, WINDOW_HEIGHT, (100, WINDOW_HEIGHT - 532), (80, 0), (0, 0), p[1])    
            else:
                return characters.Dinosaur(WINDOW_WIDTH, WINDOW_HEIGHT, (660, WINDOW_HEIGHT - 532), (630, 0), (1052, 0), p[1])    
    
    def __update(self):
        self.surface.fill(BACKGROUND_COLOR)

        self.current_scene.update()
        for ojbects in self.current_scene.get_objects():
            self.surface.blit(*ojbects)

    def action_collect(self):
        action_response = self.current_scene.action_collect(self)
        if action_response is None:
            return None
        
        if action_response == True:
            self.game_state += 1
            
            if self.game_state == GAME_STATE.PLAYING:
                self.scenes.append(playing_scene([self.__create_role(ps) for ps in self.player_status]))
            
            self.current_scene = self.scenes[self.game_state]
            for k, v in self.user_input.items():
                self.user_input[k]['input'] = ''
            return True
    
        return False
      
    def start(self):  
        self.idx = 0
        while True:
            if self.idx % 1e6 == 0:
                for k, v in self.user_input.items():
                    print(k, v)
            if self.action_collect() is None:
                pygame.quit()
                break
            self.__update()

            pygame.display.update()
            self.main_clock.tick(60)
          
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    IP, port = addr
    game.user_input[f'{IP}:{port}'] = {'index': len(game.user_input), 'input': ''}
    connected = True
    try:
        while connected:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                
                
                
                if game.user_input[f'{IP}:{port}']['input'] == VOICE.START:
                    continue
                else:
                    game.user_input[f'{IP}:{port}']['input'] = int(msg)
                if msg == DISCONNECT_MESSAGE:
                    break    
                
                print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

        conn.close()
    except:
        print("DISCONNECT!")
        game.user_input.pop(f'{IP}:{port}')

def start():
    server.listen()
    
    try:
        while True:
            conn, addr = server.accept()
            thread = threading.Thread(target=handle_client, args=(conn, addr))
            thread.start()
    except KeyboardInterrupt:
        print("[SHUTTING DOWN] Server is shutting down.")
    finally:
        server.close()


game = MainGame(WINDOW_WIDTH, WINDOW_HEIGHT, BACKGROUND_COLOR)

if __name__ == '__main__':
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(ADDR)
    
    threading.Thread(target = start).start()
    
    
    game.start()
    print('game start!')
    