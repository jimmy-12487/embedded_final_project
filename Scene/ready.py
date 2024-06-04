import pygame
from Characters.characters import *
from pygame.locals import *
from enums import *


WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800

class player_choosing:
    def __init__(self, is_left):
        self.pick_states = ['chick', 'dino_picked']
        self.ready = False
        self.is_left = is_left
        self.available_characters_raw = [pygame.image.load(f'Ready/{state}.png').convert_alpha() for state in self.pick_states]
        self.rect = (0, 0)
        
        self.ready_image = pygame.transform.scale(
                    pygame.image.load(f'Ready/ready.png').convert_alpha(), (300, 180))
        
    def update(self):
        self.available_characters_raw = [pygame.image.load(f'Ready/{state}.png').convert_alpha() for state in self.pick_states]
        self.available_characters = [pygame.transform.scale(r, (150, 150)) for r in self.available_characters_raw]
        
        if 'chick_picked' in self.pick_states:
            self.character = self.main_image = pygame.transform.scale(
                        pygame.image.load(f'./Characters/Chicken/init_0.png').convert_alpha(), (300, 300))
            self.rect = (100, WINDOW_HEIGHT - 412)
            
        elif 'dino_picked' in self.pick_states:
            self.character = self.main_image = pygame.transform.scale(
                        pygame.image.load(f'./Characters/Dinosaur/init_0.png').convert_alpha(), (450, 450))
            self.rect = (100, WINDOW_HEIGHT - 532)
        
        
        
        if not self.is_left:
            self.character = pygame.transform.flip(self.character, True, False)
            self.rect = (self.rect[0] + 560, self.rect[1])
    
    def get_objects(self):
        objects = [(self.character, self.rect)]
        if self.is_left:
            objects += [(c, (100 + 150*i, 100)) for i, c in enumerate(self.available_characters)]
            
        else:
            objects += [(c, (900 + 150*i, 100)) for i, c in enumerate(self.available_characters)]
        
        if self.ready:
            objects += [(self.ready_image, (self.rect[0] + 50, self.rect[1] + 250))]            
        
        return objects
        
        
            
class ready_scene:
    def __init__(self):
        self.num_players = 2
        self.players = [player_choosing(i==0) for i in range(self.num_players)]
        
    def update(self):
        for p in self.players:
            p.update()  
    
    def action_collect(self, main_scene):
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            
            if event.type != KEYDOWN:
                continue
            
            e = event.dict['key']
            
            if e == K_RETURN:
                main_scene.player_status = [(0, p.is_left) if 'chick_picked' in p.pick_states else (1, p.is_left) for p in self.players]
                return True
            
        for v in main_scene.user_input.values():
            if self.players[v['index']].ready:
                continue
            print(v)
            if v['input'] == VOICE.READY:
                self.players[v['index']].ready = True
            elif v['input'] == VOICE.CHICK:
                self.players[v['index']].pick_states = ['chick_picked', 'dino']
            elif v['input'] == VOICE.DINO:
                self.players[v['index']].pick_states = ['chick', 'dino_picked']
                
        return False
    
    def get_objects(self):
        
        return self.players[0].get_objects() + self.players[1].get_objects()
    
        