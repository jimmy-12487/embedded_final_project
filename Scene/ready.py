import pygame
from Characters.characters import *
from pygame.locals import *
from enums import *
from configs import *

class player_choosing:
    def __init__(self, is_left):
        if is_left:
            self.pick_states = ['chick_picked', 'dino']
        else:
            self.pick_states = ['chick', 'dino_picked']
        self.ready = False
        self.position = 'LEFT' if is_left else 'RIGHT'
        self.available_characters_raw = [pygame.image.load(f'Ready/{state}.png').convert_alpha() for state in self.pick_states]
        
        self.ready_image = pygame.transform.scale(pygame.image.load(f'Ready/ready.png').convert_alpha(), (300, 180))
        
    def update(self):
        self.available_characters_raw = [pygame.image.load(f'Ready/{state}.png').convert_alpha() for state in self.pick_states]
        self.available_characters = [pygame.transform.scale(r, (AVAIABLE_ICON_SIZE, AVAIABLE_ICON_SIZE)) for r in self.available_characters_raw]
        
        if 'chick_picked' in self.pick_states:
            self.character = pygame.transform.scale( pygame.image.load(f'./Characters/Chicken/init_0.png').convert_alpha(), (CHICKEN_WIDTH, CHICKEN_HEIGHT))
            self.rect = (CHICKEN_INIT_POSITION[self.position]['X'], CHICKEN_INIT_POSITION[self.position]['Y'])
                
        elif 'dino_picked' in self.pick_states:
            self.character = pygame.transform.scale(pygame.image.load(f'./Characters/Dinosaur/init_0.png').convert_alpha(), (DINO_WIDTH, DINO_HEIGHT))
            self.rect = (DINO_INIT_POSITION[self.position]['X'], DINO_INIT_POSITION[self.position]['Y'])
        
        if self.position == 'RIGHT':
            self.character = pygame.transform.flip(self.character, True, False)
    
    def get_objects(self):
        objects = [(self.character, self.rect)]
        if self.position == 'LEFT':
            objects += [(c, (WALL_OFFSET + AVAIABLE_ICON_SIZE*i, WALL_OFFSET)) for i, c in enumerate(self.available_characters)]
            
        else:
            objects += [(c, (WINDOW_WIDTH - WALL_OFFSET - AVAIABLE_ICON_SIZE*i, WALL_OFFSET)) for i, c in enumerate(self.available_characters, 1)]
        
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
                main_scene.player_status = [(0, p.position) if 'chick_picked' in p.pick_states else (1, p.position) for p in self.players]
                return True
            
        for v in main_scene.user_input.values():
            if self.players[v['index']].ready:
                continue
            
            if v['input'] == VOICE.READY:
                self.players[v['index']].ready = True
            elif v['input'] == VOICE.CHICK:
                self.players[v['index']].pick_states = ['chick_picked', 'dino']
            elif v['input'] == VOICE.DINO:
                self.players[v['index']].pick_states = ['chick', 'dino_picked']
                
        return False
    
    def get_objects(self):
        
        return self.players[0].get_objects() + self.players[1].get_objects()
    
        