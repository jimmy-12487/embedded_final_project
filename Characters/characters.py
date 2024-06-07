import pygame
import os
from enums import *
from configs import *

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
        
        self.state = STATES.INIT
        self.next_state = STATES.IDLE
        
        self.direction = DIRECTION.STILL
        self.next_direction = DIRECTION.STILL
        
        self.attack_state = ATTACK_MOVEMENT.NONE
        self.next_attack_state = ATTACK_MOVEMENT.NONE
        
        self.health_bar_topleft = HEALTH_BAR_POSITION[self.position]['X'], HEALTH_BAR_POSITION[self.position]['Y']
        self.health_bar_icon_topleft = HEALTH_BAR_ICON_POSITION[self.position]['X'], HEALTH_BAR_ICON_POSITION[self.position]['Y']
        
        self.state_counter = 0
        
        self.ticks = 0
        self.movement_counter = 0
        
        self.x_movements, self.y_movements = 0, 0
        
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
            
            if self.position == 'LEFT' :
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
            (HEALTH_BAR_WIDTH, HEALTH_BAR_HIEGHT)
        )
        
    def __make_health_icon_image(self):
        self.health_icon_image = pygame.transform.scale(
            pygame.image.load(f'{self.path}/health_bar.png').convert_alpha(),
            (HEALTH_BAR_ICON_SIZE, HEALTH_BAR_ICON_SIZE)
        )
    
    
    def __make_attack_image(self):
        if self.attack_state != ATTACK_MOVEMENT.NONE:
            self.attack_image = pygame.transform.scale(
                pygame.image.load(f'{self.path}/{self.attack_state.name.lower()}_0.png').convert_alpha(), 
                (300, 180)
            )
        else:
            self.attack_image = None
            
    def set_next_states(self, next_state = STATES.IDLE, next_direction = DIRECTION.STILL, next_attack_state = ATTACK_MOVEMENT.NONE):
        self.next_state = next_state
        self.next_direction = next_direction
        self.next_attack_state = next_attack_state
        
    def move(self):    
        self.x_position, self.y_position = self.x_position + self.x_movements, self.y_position + self.y_movements
        
        self.update_movement()
        
    
    def update_movement(self):
        if self.movement_counter != TICKS_PER_MOVEMENT:
            self.movement_counter += 1
            return 
        
        if self.state == STATES.ATTACK and self.attack_state == ATTACK_MOVEMENT.ATTACK2:
            if self.direction == DIRECTION.STILL:
                self.x_movements, self.y_movements = 0, 0
            elif self.direction == DIRECTION.LEFT:
                self.x_movements, self.y_movements = -MOVEMENT_SPEED, 0
            elif self.direction == DIRECTION.RIGHT:
                self.x_movements, self.y_movements = MOVEMENT_SPEED, 0
        else:
            self.x_movements, self.y_movements = 0, 0
            
        self.movement_counter = 0
            
    def update_state(self):
        if self.ticks != TICKS_PER_FRAME:
            self.ticks += 1
            if self.state != STATES.IDLE or self.next_state == STATES.IDLE:
                return
        
        self.ticks = 0
        
        if self.state != self.next_state:
            self.state_counter = 0
        
        self.state = self.next_state
        self.direction = self.next_direction
        self.attack_state = self.next_attack_state

        self.update_animation()
        
    def update_animation(self):

        self.__make_main_image()
        self.__make_health_image()        
        self.__make_attack_image()
        
        self.state_counter += 1
        if self.state_counter >= self.state_frame_num[self.state.name]:
            self.state_counter = 0
    
    def update(self):
        self.move()
        self.update_state()
        
        
    def get_objects(self):
        objects = []
        if self.position == 'LEFT':
            objects += [(self.main_image, (self.x_position, self.y_position)), 
                        (self.health_image, self.health_bar_topleft), 
                        (self.health_icon_image, self.health_bar_icon_topleft)]
        else:
            objects += [(pygame.transform.flip(self.main_image, True, False), (self.x_position, self.y_position)),
                        (pygame.transform.flip(self.health_image, True, False), self.health_bar_topleft),   
                        (pygame.transform.flip(self.health_icon_image, True, False), self.health_bar_icon_topleft)
                        ]
            
        if self.attack_image is not None:
            if self.position == 'LEFT':
                objects.append((self.attack_image, self.__where_is_mouth()))
            else:
                objects.append((pygame.transform.flip(self.attack_image, True, False), self.__where_is_mouth()))
        return objects
    
class Chicken(GameObject, pygame.sprite.Sprite):
    
    def __init__(self, position='LEFT'):
        
        self.path = './Characters/Chicken'
        self.race = 'chick'
        self.position = position
    
        self.x_position, self.y_position = CHICKEN_INIT_POSITION[position]['X'], CHICKEN_INIT_POSITION[position]['Y']
        
        self.width, self.height = CHICKEN_WIDTH, CHICKEN_HEIGHT
        
        self.health, self.health_unit = 100, 10
    
        
        super().__init__()
        
class Dinosaur(GameObject, pygame.sprite.Sprite):
    
    def __init__(self, position='LEFT'):
        
        self.path = './Characters/Dinosaur'
        self.race = 'dino'
        self.position = position
        
        self.x_position, self.y_position = DINO_INIT_POSITION[position]['X'], DINO_INIT_POSITION[position]['Y']
        
        self.width, self.height = DINO_WIDTH, DINO_HEIGHT
        
        self.health, self.health_unit = 200, 20
        
        
        
        
        super().__init__()
        