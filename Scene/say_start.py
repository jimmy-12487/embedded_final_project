import pygame
from pygame.locals import *
from enums import *

class say_start_scene:
    def __init__(self):
        self.say_start_raw = pygame.image.load(f'SayStart/say_start.png').convert_alpha()
        self.say_start_raw_alpha = 0
        self.say_start_raw_direction = 1
        self.say_start_raw_stride = 5
        self.say_start_raw_rect = (300, 500)
        
        self.say_start = pygame.transform.scale(self.say_start_raw, (600, 150))
        pass
    
    def update(self):
        self.say_start_raw.set_alpha(self.say_start_raw_alpha)
        
        self.say_start_raw_alpha += self.say_start_raw_direction * self.say_start_raw_stride
        
        if self.say_start_raw_alpha > 255:
            self.say_start_raw_alpha = 255
            self.say_start_raw_direction = -1
            
        elif self.say_start_raw_alpha < 0:
            self.say_start_raw_alpha = 0
            self.say_start_raw_direction = 1
            
        self.say_start = pygame.transform.scale(self.say_start_raw, (600, 150))

    def action_collect(self, main_scene):
        for event in pygame.event.get():
            if event.type == QUIT:
                return None 
            if event.type != KEYDOWN:
                continue
            
            e = event.dict['key']
            
            if e == K_RETURN:
                return True
            
        
        return all(v['input'] == VOICE.START for v in main_scene.user_input.values()) and len(main_scene.user_input) >= 2
        

    def get_objects(self):
        
        return [(self.say_start, self.say_start_raw_rect)]

if __name__ == '__main__':
    st = say_start_scene()