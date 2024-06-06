import pygame
import os
from enums import *

ANIMATION_FRAMES = 20
MOVEMENT_FRAMES = 5
PIXEL = 1

class GameObject():
    def __init__(self):
        self.images_rect = {}
        
        self.main_image = pygame.transform.scale(
                                pygame.image.load(f'{self.path}/init_0.png').convert_alpha(),
                                (self.width, self.height))
        
        self.main_rect = self.main_image.get_rect()
        self.main_rect.topleft = self.main_topleft
        self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/100.png').convert_alpha(),
                            (512, 64))
        self.health_rect = self.health_image.get_rect()
        self.health_rect.topleft = self.health_bar_topleft
        
        self.health_icon_image = pygame.transform.scale(
                                pygame.image.load(f'{self.path}/health_bar.png').convert_alpha(),
                            (160, 160))

        self.health_icon_rect = self.health_icon_image.get_rect()
        self.health_icon_rect.topleft = self.health_bar_icon_topleft
        
        self.images_rect['main'] = (self.main_image, self.main_rect)
        self.images_rect['health'] = (self.health_image, self.health_rect)
        self.images_rect['health_icon'] = (self.health_icon_image, self.health_icon_rect)
        
        
        self.widow_width = self.widow_width
        self.window_height = self.window_height
        
        self.state = STATES.INIT
        self.next_state = STATES.IDLE
        
        self.direction = DIRECTION.STILL
        self.next_direction = DIRECTION.STILL
        
        self.state_counter = 0
        self.state_animation_frame_counter = 0
        self.movement_frame_counter = 0
        
        self.movements = (0, 0)
        
        self.state_frame_num = {}
        
        for state in STATES:
            if self.state_frame_num.get(state.name, None) is None:
                self.state_frame_num[state.name] = 0
                
        for file in os.listdir(self.path):
            for k in self.state_frame_num.keys():
                if file.startswith(k.lower()):
                    self.state_frame_num[k] += 1

        print(self.state_frame_num)
    
    def update_movement(self):
        
        if self.direction == DIRECTION.STILL:
           self.movements = (0, 0) 
           
        self.main_rect.topleft = tuple(position + movement for position, movement in zip(self.main_rect.topleft, self.movements))
        
        if self.movement_frame_counter != MOVEMENT_FRAMES:
            self.movement_frame_counter += 1
            return 
        
        self.movement_frame_counter = 0
        
        if self.state == STATES.MOVING:
            if self.direction == DIRECTION.STILL:
                self.movements = (0, 0)
            elif self.direction == DIRECTION.LEFT:
                self.movements = (-PIXEL, 0)
            elif self.direction == DIRECTION.RIGHT:
                self.movements = (PIXEL, 0)
        

    
    def update_state(self):
        if self.state != self.next_state:
            self.state_counter = 0
        self.state, self.next_state = self.next_state, STATES.IDLE
        self.direction, self.next_direction = self.next_direction, DIRECTION.STILL
    
    def update_animation(self):
        if self.state_animation_frame_counter != ANIMATION_FRAMES:
            self.state_animation_frame_counter += 1
            if self.state != STATES.IDLE or self.next_state == STATES.IDLE:
                return
        self.update_state()
        if self.health/self.init > 0.9:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/100.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0.8:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/90.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0.7:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/80.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0.6:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/70.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0.5:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/60.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0.4:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/50.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0.3:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/40.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0.2:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/30.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0.1:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/20.png').convert_alpha(),
                            (512, 64))
        elif self.health/self.init > 0:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/10.png').convert_alpha(),
                            (512, 64))
        else:
            self.health_image = pygame.transform.scale(
                                pygame.image.load(f'./Characters/Health/0.png').convert_alpha(),
                            (512, 64))
        self.main_image = pygame.transform.scale(
            pygame.image.load(f'{self.path}/{self.state.name.lower()}_{self.state_counter}.png').convert_alpha(), 
            (self.width, self.height)
        )
        
        self.state_animation_frame_counter = 0
        self.state_counter += 1
        if self.state_counter >= self.state_frame_num[self.state.name]:
            self.state_counter = 0
    
    def update(self):
        self.update_movement()
        self.update_animation()
        
        
        
        self.images_rect['main'] = (self.main_image, self.main_rect)
        self.images_rect['health'] = (self.health_image, self.health_rect)
        self.images_rect['health_icon'] = (self.health_icon_image, self.health_icon_rect)
        

            
class Chicken(GameObject, pygame.sprite.Sprite):
    
    def __init__(self, widow_width, window_height, main_topleft, health_bar_topleft, health_bar_icon_topleft, is_left=True):
        
        self.path = './Characters/Chicken'
        self.main_topleft = main_topleft
        self.widow_width = widow_width
        self.window_height = window_height
        self.width = 300
        self.height = 300
        self.health_init = 100
        self.health = 100
        self.health_bar_topleft = health_bar_topleft
        self.health_bar_icon_topleft = health_bar_icon_topleft
        self.is_left = is_left
        super().__init__()
        
class Dinosaur(GameObject, pygame.sprite.Sprite):
    
    def __init__(self, widow_width, window_height, main_topleft, health_bar_topleft, health_bar_icon_topleft, is_left=True):
        
        self.path = './Characters/Dinosaur'
        self.main_topleft = main_topleft
        self.widow_width = widow_width
        self.window_height = window_height
        self.width = 450
        self.height = 450
        self.health = 200
        self.health_init = 200
        self.health_bar_topleft = health_bar_topleft
        self.health_bar_icon_topleft = health_bar_icon_topleft
        self.is_left = is_left
        super().__init__()