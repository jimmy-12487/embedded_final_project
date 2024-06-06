import pygame
import os
from enums import *

ANIMATION_FRAMES = 20
MOVEMENT_FRAMES = 5
PIXEL = 1

DINO_ATTACK1_X_LEFT_OFFSET = 20

# ** TODO
class GameObjectState():
    def __init__(self):
        self.state = STATES.INIT
        self.next_state = STATES.IDLE
        
        self.direction = DIRECTION.STILL
        self.next_direction = DIRECTION.STILL
        
        self.attack_state = ATTACK_MOVEMENT.NONE
        self.next_attack_state = ATTACK_MOVEMENT.NONE

    def update(self):
        self.state, self.next_state = self.next_state, STATES.IDLE
        self.direction, self.next_direction = self.next_direction, DIRECTION.STILL
        self.attack_state, self.next_attack_state = self.next_attack_state, ATTACK_MOVEMENT.NONE


class GameObject():
    def __init__(self):
        self.attack_image = None

        self.widow_width = self.widow_width
        self.window_height = self.window_height
        
        self.state = STATES.INIT
        self.next_state = STATES.IDLE
        
        self.direction = DIRECTION.STILL
        self.next_direction = DIRECTION.STILL
        
        self.attack_state = ATTACK_MOVEMENT.NONE
        self.next_attack_state = ATTACK_MOVEMENT.NONE
        
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
                if file.startswith(f'{k.lower()}_'):
                    self.state_frame_num[k] += 1

        self.__make_main_image()
        self.__make_health_image()
        self.__make_health_icon_image()

    def __where_is_mouth(self):
        if self.race == 'chick':
            pass
        elif self.race == 'dino':
            x_offset = 50  
            y_offset = 50
            
            if self.is_left:
                return (self.x_position + 300, self.y_position + y_offset)
            else:
                return (self.x_position - 150, self.y_position + y_offset)
        
    def __make_main_image(self):
        self.main_image = pygame.transform.scale(
            pygame.image.load(f'{self.path}/{self.state.name.lower()}_{self.state_counter}.png').convert_alpha(), 
            (self.width, self.height)
        )
        self.main_rect = self.main_image.get_rect()
        self.main_rect.topleft = (self.x_position, self.y_position)
    
    def __make_health_image(self):
        self.health_image = pygame.transform.scale(
            pygame.image.load(f'./Characters/Health/{(self.health // self.health_unit) * 10}.png').convert_alpha(),
            (512, 64)
        )
        self.health_rect = self.health_image.get_rect()
        self.health_rect.topleft = self.health_bar_topleft
        
    def __make_health_icon_image(self):
        self.health_icon_image = pygame.transform.scale(
            pygame.image.load(f'{self.path}/health_bar.png').convert_alpha(),
            (160, 160)
        )
        
        self.health_icon_rect = self.health_icon_image.get_rect()
        self.health_icon_rect.topleft = self.health_bar_icon_topleft
    
    def __make_attack_image(self):
        if self.attack_state != ATTACK_MOVEMENT.NONE:
            self.attack_image = pygame.transform.scale(
                pygame.image.load(f'{self.path}/{self.attack_state.name.lower()}_0.png').convert_alpha(), 
                (300, 180)
            )
        else:
            self.attack_image = None
    
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
        print(self.state)
        if self.state != self.next_state:
            self.state_counter = 0
        self.state = self.next_state
        if self.state == STATES.DIE:
            self.next_state = STATES.DIE
        else:
            self.next_state = STATES.IDLE
        self.direction, self.next_direction = self.next_direction, DIRECTION.STILL
        self.attack_state, self.next_attack_state = self.next_attack_state, ATTACK_MOVEMENT.NONE
    
    def update_animation(self):
        if self.state_animation_frame_counter != ANIMATION_FRAMES:
            self.state_animation_frame_counter += 1
            if self.state != STATES.IDLE or self.next_state == STATES.IDLE:
                return
        
        self.update_state()
        self.__make_main_image()
        self.__make_health_image()        
        self.__make_attack_image()

            
        self.state_animation_frame_counter = 0
        self.state_counter += 1
        if self.state_counter >= self.state_frame_num[self.state.name]:
            self.state_counter = 0
    
    def update(self):
        # self.update_movement()
        self.update_animation()
        
    def get_objects(self):
        objects = []
        if self.is_left:
            objects += [(self.main_image, (self.x_position, self.y_position)), (self.health_image, self.health_rect), (self.health_icon_image, self.health_icon_rect)]
        else:
            objects += [(pygame.transform.flip(self.main_image, True, False), (self.x_position, self.y_position)),
                        (pygame.transform.flip(self.health_image, True, False), self.health_rect),   
                        (pygame.transform.flip(self.health_icon_image, True, False), self.health_icon_rect)
                        ]
            
        if self.attack_image is not None:
            if self.is_left:
                objects.append((self.attack_image, self.__where_is_mouth()))
            else:
                objects.append((pygame.transform.flip(self.attack_image, True, False), self.__where_is_mouth()))
        return objects
    
class Chicken(GameObject, pygame.sprite.Sprite):
    
    def __init__(self, widow_width, window_height, main_topleft, health_bar_topleft, health_bar_icon_topleft, is_left=True):
        
        self.path = './Characters/Chicken'
        self.race = 'chick'
        
        self.x_position, self.y_position = main_topleft
        self.widow_width = widow_width
        self.window_height = window_height
        
        self.width = 300
        self.height = 300
        
        self.health = 100
        self.health_unit = 10
        
        self.health_bar_topleft = health_bar_topleft
        self.health_bar_icon_topleft = health_bar_icon_topleft
        
        self.is_left = is_left
        
        super().__init__()
        
class Dinosaur(GameObject, pygame.sprite.Sprite):
    
    def __init__(self, widow_width, window_height, main_topleft, health_bar_topleft, health_bar_icon_topleft, is_left=True):
        
        self.path = './Characters/Dinosaur'
        self.race = 'dino'
        
        self.x_position, self.y_position = main_topleft
        
        self.widow_width = widow_width
        self.window_height = window_height
        self.width = 450
        self.height = 450
        
        self.health = 200
        self.health_unit = 20
        
        self.health_bar_topleft = health_bar_topleft
        self.health_bar_icon_topleft = health_bar_icon_topleft
        self.is_left = is_left
        
        super().__init__()
        