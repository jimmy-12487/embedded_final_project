import pygame
from pygame.locals import *
from enums import *
from configs import *


class say_start_scene:
    def __init__(self):
        self.say_start_raw = pygame.image.load(f'SayStart/say_start.png').convert_alpha()
        self.say_start_raw_alpha = 0
        self.say_start_raw_direction = 1
        self.say_start_raw_stride = 5
        self.say_start_raw_rect = (WINDOW_WIDTH // 3, 550)
        self.title_0_raw = pygame.image.load(f'SayStart/title_1.png').convert_alpha()
        self.title_1_raw = pygame.image.load(f'SayStart/title_0.png').convert_alpha()
        self.start = 0
        self.title_rect = (WINDOW_WIDTH // 3, 45)
        self.counter = 0
        
        self.say_start = pygame.transform.scale(self.say_start_raw, (600, 150))
        self.title_0 = pygame.transform.scale(self.title_0_raw, (500, 500))
        self.title_1 = pygame.transform.scale(self.title_1_raw, (500, 500))
        self.title = [self.title_0, self.title_1]
        self.title_idx = 0

        pass
    
    def update(self):
        self.say_start_raw.set_alpha(self.say_start_raw_alpha)
        
        self.say_start_raw_alpha += self.say_start_raw_direction * self.say_start_raw_stride
        
        if self.start == 1:
            self.say_start_raw_alpha = 0
        
        elif self.say_start_raw_alpha > 255:
            self.say_start_raw_alpha = 255
            self.say_start_raw_direction = -1
            
        elif self.say_start_raw_alpha < 0:
            self.say_start_raw_alpha = 0
            self.say_start_raw_direction = 1
            
        self.say_start = pygame.transform.scale(self.say_start_raw, (600, 150))
        
        if self.start == 1:
            self.counter += 1
            if self.counter % 5 == 0:
                if self.title_idx == 1:
                    self.title_idx = 0
                else:
                    self.title_idx = 1

    def action_collect(self, main_scene):
        if self.counter == 1:
            select_sound = pygame.mixer.Sound("sounds/select.wav")
            select_sound.play()
        if self.counter == 60:
            return True
        for event in pygame.event.get():
            if event.type == QUIT:
                return None 
            if event.type != KEYDOWN:
                continue
            
            e = event.dict['key']
            
            if e == K_RETURN and self.start == 0:
                self.say_start_raw_alpha = 255
                self.start = 1
            
        if all(v['input'] == VOICE.START for v in main_scene.user_input.values()) and len(main_scene.user_input) >= 2:
            for k, v in main_scene.user_input.items():
                main_scene.user_input[k]['input'] = ''
            return True
            
        return False
        

    def get_objects(self):
        return [(self.say_start, self.say_start_raw_rect), (self.title[self.title_idx], self.title_rect)]

if __name__ == '__main__':
    st = say_start_scene()