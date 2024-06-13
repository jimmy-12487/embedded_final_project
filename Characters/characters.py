import pygame
import os
import random
import math
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
        self.defend_image = None
        self.state = STATES.INIT
        self.next_state = STATES.IDLE
        
        self.direction = DIRECTION.STILL
        self.next_direction = DIRECTION.STILL
        
        self.attack_state = ATTACK_MOVEMENT.NONE
        self.next_attack_state = ATTACK_MOVEMENT.NONE
        
        self.volumn = 0
        self.next_volumn = 0
        
        self.ticks = 0
        
        self.health_bar_topleft = HEALTH_BAR_POSITION[self.position]['X'], HEALTH_BAR_POSITION[self.position]['Y']
        self.health_bar_icon_topleft = HEALTH_BAR_ICON_POSITION[self.position]['X'], HEALTH_BAR_ICON_POSITION[self.position]['Y']
        
        self.attack_left_position, self.attack_right_position = self.x_position, self.x_position + self.width
        
        self.user_input = {}
        
        self.state_counter = 0
        self.hurt_in_this_frame = False
        self.damage_tick = 0
        
        self.movement_counter = 0
        
        self.x_movements, self.y_movements = 0, 0
        self.dmg_img = []
        self.state_frame_num = {}
        self.state_interupt = False
        
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

    def update_state_interupt(self):
        if self.state == STATES.IDLE:
            if self.user_input != {} or self.next_state != STATES.IDLE:
                self.state_interupt = True
            
    def __far_attack(self):
        if self.race == 'chick' and self.attack_state == ATTACK_MOVEMENT.ATTACK1:
            if self.position == 'LEFT':
                self.egg_x_position += 50
            else:
                self.egg_x_position -= 50
            self.attack_left_position, self.attack_right_position = self.egg_x_position, self.egg_x_position + CHICKEN_EGG_WIDTH
            
    def __next_frame(self):
        if self.ticks != TICKS_PER_FRAME:
            if self.state == STATES.DEFENDING:
                self.ticks += 0.5
            elif self.attack_state == ATTACK_MOVEMENT.ATTACK1:
                self.ticks += 1
            elif self.race == 'chick':
                self.ticks += 2
            else:
                self.ticks += 1
            return False
        
        return True
    
    def __where_is_shield(self):
        if self.race == 'chick':
            if self.position == 'LEFT' :
                return (self.x_position + self.width - 100, self.y_position - 150)
            else:
                return (self.x_position - 100, self.y_position - 150)
        elif self.race == 'dino':
            if self.position == 'LEFT' :
                return (self.x_position + self.width - 200, self.y_position)
            else:
                return (self.x_position - 100, self.y_position)
            

    def __where_is_mouth(self):
        if self.race == 'chick':
            if self.position == 'LEFT' :
                return (self.x_position + self.width - 100, self.y_position)
            else:
                return (self.x_position - CHICKEN_EGG_WIDTH, self.y_position)
        elif self.race == 'dino':
            if self.position == 'LEFT' :
                return (self.x_position + self.width - 200, self.y_position)
            else:
                return (self.x_position + 200, self.y_position)
    
    def __where_is_fire(self):
        if self.race == 'chick':    
            x, y = self.__where_is_mouth()
            if self.position == 'LEFT':
                return (x, y)
            else:
                return (x - CHICKEN_EGG_WIDTH, y)
        elif self.race == 'dino':    
            x, y = self.__where_is_mouth()
            if self.position == 'LEFT':
                return (x, y)
            else:
                return (x - DINO_FIRE_WIDTH, y)
    
    def __make_main_image(self):
        self.main_image = pygame.transform.scale(
            pygame.image.load(f'{self.path}/{self.state.name.lower()}_{self.state_counter}.png').convert_alpha(), 
            (self.width, self.height)
        )
        self.main_rect = self.main_image.get_rect()
        self.main_rect.topleft = (self.x_position, self.y_position)
    
    def __make_health_image(self):
        if self.health <= 0:
            self.health_image = pygame.transform.scale(
                pygame.image.load(f'./Characters/Health/0.png').convert_alpha(),
                (HEALTH_BAR_WIDTH, HEALTH_BAR_HIEGHT)
            )   
            return 
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
        if self.race == 'dino':
            if self.state == STATES.ATTACK:
                attack_raw = pygame.image.load(f'{self.path}/{self.attack_state.name.lower()}_0.png').convert_alpha()
                if self.attack_state == ATTACK_MOVEMENT.ATTACK1:
                    self.attack_image = pygame.transform.scale(attack_raw, (DINO_FIRE_WIDTH, DINO_FIRE_HEIGHT))
                else:
                    self.attack_image = pygame.transform.scale(attack_raw, (DINO_SCRATCH_WIDTH, DINO_SCRATCH_HEIGHT))
                return
        elif self.race == 'chick':
            if self.state == STATES.ATTACK:
                attack_raw = pygame.image.load(f'{self.path}/{self.attack_state.name.lower()}_0.png').convert_alpha()
                if self.attack_state == ATTACK_MOVEMENT.ATTACK1:
                    if not self.deal_damage_in_this_frame:
                        self.attack_image = pygame.transform.scale(attack_raw, (CHICKEN_EGG_WIDTH, CHICKEN_EGG_HEIGHT))
                    else:
                        self.attack_image = None
                else:
                    self.attack_image = pygame.transform.scale(attack_raw, (CHICKEN_RUSH_WIDTH, CHICKEN_RUSH_HEIGHT))
                return 
        
        self.attack_image = None
            
    def __make_defend_image(self):
        if self.state == STATES.DEFENDING:
            defend_raw = pygame.image.load(f'{self.path}/defend_0.png').convert_alpha()
            self.defend_image = pygame.transform.scale(defend_raw, (DEFEND_WIDTH, DEFEND_HEIGHT))
        else:
            self.defend_image = None
        
    def __collide_with_it(self, _it):
        if self.position == 'LEFT' and self.attack_right_position >= _it.x_position:
            
            return True
        if self.position == 'RIGHT' and self.attack_left_position <= _it.x_position + _it.width:
            return True
        
        return False
    
    def __back_to_initial(self):
        if self.position == 'LEFT':
            return self.x_position < self.initial_x_position
        else:
            return self.x_position > self.initial_x_position
    
    def __make_damage_image(self, dmg):
        self.dmg_img = []
        
        for character in f'{dmg}':
            print(character)
            self.dmg_img.append(
                pygame.transform.scale(
                    pygame.image.load(f'./Characters/DamageFont/{character}.png').convert_alpha(),
                    (FONT_SIZE, FONT_SIZE)
                ))
        print(self.dmg_img)
        
    def set_next_states(self, _it,
                        next_state = STATES.IDLE,
                        next_direction = DIRECTION.STILL,
                        next_attack_state = ATTACK_MOVEMENT.NONE,
                        next_volumn = 0):
        
        if self.health <= 0:
            self.next_state, self.next_direction, self.next_attack_state = STATES.DIE, DIRECTION.STILL, ATTACK_MOVEMENT.NONE
            return    
        self.__far_attack()
        response = self.interaction(_it)
        
        if response == INTERACTION_RESPONSE.NONE:
            if self.user_input == {}:
                self.next_state, self.next_direction, self.next_attack_state, self.next_volumn = next_state, next_direction, next_attack_state, next_volumn
            else:
                self.next_state, self.next_direction, self.next_attack_state, self.next_volumn = self.user_input['state'], self.user_input['direction'], self.user_input['attack_movement'], self.user_input['volumn']

        elif response == INTERACTION_RESPONSE.FORWARD_AND_COLLIDE:
            self.next_state, self.next_direction, self.next_attack_state, self.next_volumn = STATES.ATTACK, self.direction, self.attack_state, self.volumn
        elif response == INTERACTION_RESPONSE.FORWARD_NOT_COLLIDE:
            self.next_state, self.next_direction, self.next_attack_state, self.next_volumn = self.state, self.direction, self.attack_state, self.volumn
        elif response == INTERACTION_RESPONSE.ATTACK1:
            self.deal_damage(_it, self.attack1_damage)
            self.next_state, self.next_direction, self.next_attack_state, self.next_volumn = STATES.IDLE, DIRECTION.STILL, ATTACK_MOVEMENT.NONE, self.volumn
        elif response == INTERACTION_RESPONSE.ATTACK2:
            power = math.sqrt(abs(self.x_position - self.initial_x_position) / abs(self.initial_x_position - _it.initial_x_position) )
            self.deal_damage(_it, int(self.attack2_damage * power))
            self.next_state, self.next_direction, self.next_attack_state, self.next_volumn = STATES.RETREAT, self.direction, ATTACK_MOVEMENT.NONE, self.volumn
        elif response == INTERACTION_RESPONSE.RETREAT_AND_GO_BACK:
            self.state_interupt = True
            self.next_state, self.next_direction, self.next_attack_state, self.next_volumn = STATES.IDLE, DIRECTION.STILL, ATTACK_MOVEMENT.NONE, 0
        elif response == INTERACTION_RESPONSE.RETREAT_NOT_GO_BACK:
            self.next_state, self.next_direction, self.next_attack_state, self.next_volumn = self.state, self.direction, self.attack_state, 0
            
                
            
        self.user_input = {}    
        
    def deal_damage(self, _it, dmg):
        if self.deal_damage_in_this_frame:
            return  
        _it.handle_damage(dmg)
        self.deal_damage_in_this_frame = True
        
    def handle_damage(self, dmg):
        
        if self.state == STATES.DEFENDING:
            return
        self.damage_tick = 1
        self.hurt_in_this_frame = True
        dmg = min(dmg, self.health)
        self.__make_damage_image(dmg)
        
        self.health -= dmg
    
    def interaction(self, _it):
        if self.state == STATES.FORWARD:
            if self.__collide_with_it(_it):
                return INTERACTION_RESPONSE.FORWARD_AND_COLLIDE
            else:
                return INTERACTION_RESPONSE.FORWARD_NOT_COLLIDE
        
        if self.state == STATES.RETREAT:
            if self.__back_to_initial():
                return INTERACTION_RESPONSE.RETREAT_AND_GO_BACK
            else:
                return INTERACTION_RESPONSE.RETREAT_NOT_GO_BACK
        
        elif self.state == STATES.ATTACK and self.__collide_with_it(_it):
            if self.attack_state == ATTACK_MOVEMENT.ATTACK1:
                return INTERACTION_RESPONSE.ATTACK1
            else:
                return INTERACTION_RESPONSE.ATTACK2
        
        return INTERACTION_RESPONSE.NONE
    
    def move(self):
        if self.state == STATES.FORWARD or self.state == STATES.RETREAT:
            self.x_position, self.y_position = self.x_position + self.x_movements, self.y_position + self.y_movements
            
            
    def update_movement(self):
        if self.movement_counter != TICKS_PER_MOVEMENT:
            self.movement_counter += 1
            return 
        
        if self.direction == DIRECTION.STILL:
            self.x_movements, self.y_movements = 0, 0
        elif self.direction == DIRECTION.LEFT:
            self.x_movements, self.y_movements = -MOVEMENT_SPEED, 0
        elif self.direction == DIRECTION.RIGHT:
            self.x_movements, self.y_movements = MOVEMENT_SPEED, 0
        
        if self.race == 'chick':
            self.x_movements = 3 * self.x_movements
            
        if self.state == STATES.RETREAT:
            self.x_movements = - 2 * self.x_movements
            
        self.movement_counter = 0
            
    def update_state(self):
        
        if 0 < self.damage_tick <= 20:
            self.damage_tick += 1
        else:
            self.damage_tick = 0
        
        if not self.state_interupt:
            if not self.__next_frame():
                return
        
        
        # print(f'{self.position} UPDATE STATE!')
        # print(f'RIGHT ATT: {self.attack_left_position}, STATE: {self.attack_state}')
        
        self.hurt_in_this_frame = False 
        self.deal_damage_in_this_frame = False
        self.ticks = 0  
        self.state_interupt = False
        
        if self.state != self.next_state:
            self.state_counter = 0
        else:
            self.state_counter += 1
        self.state, self.direction, self.attack_state, self.volumn = self.next_state, self.next_direction, self.next_attack_state, self.next_volumn

        if self.state_counter >= self.state_frame_num[self.state.name]:
            self.state_counter = 0        
        

        if self.race == 'chick':
            self.egg_x_position = self.__where_is_mouth()[0]
    
        

    
    def update_animation(self):

        self.__make_main_image()
        self.__make_health_image()        
        self.__make_attack_image()
        self.__make_defend_image()
        
        if self.attack_state == ATTACK_MOVEMENT.ATTACK1:
            if self.race == 'chick':
                self.attack_left_position, self.attack_right_position = self.egg_x_position, self.egg_y_position
            else:
                self.attack_left_position, self.attack_right_position  = self.__where_is_fire()[0], self.__where_is_fire()[0] + DINO_FIRE_WIDTH if self.race == 'dino' else self.x_position + CHICKEN_EGG_WIDTH                        
            

        elif self.attack_state == ATTACK_MOVEMENT.ATTACK2:
            self.attack_left_position, self.attack_right_position  = self.x_position, self.x_position + self.width 

        

    def update(self, _it):
        self.update_state_interupt()
        self.update_movement()
        self.move()
        
        self.update_state()
        self.update_animation()
        self.set_next_states(_it, STATES.IDLE, DIRECTION.STILL, ATTACK_MOVEMENT.NONE)
        
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
            
        if 1 <= self.damage_tick <= 20:
            for index, dmg in enumerate(self.dmg_img):
                objects.append((dmg, (self.x_position + FONT_SIZE*index, self.y_position - 100)))
        return objects
    
    def get_attack_animation(self):
        if self.attack_image is None:   
            return None
        
        if self.race == 'chick' and self.attack_state == ATTACK_MOVEMENT.ATTACK1:
            if self.position == 'LEFT':
                return (self.attack_image, (self.egg_x_position, self.egg_y_position))
            else:
                return (pygame.transform.flip(self.attack_image, True, False), ((self.egg_x_position, self.egg_y_position)))
        
    
        if self.position == 'LEFT':
            return (self.attack_image, self.__where_is_fire())
        else:
            return (pygame.transform.flip(self.attack_image, True, False), self.__where_is_fire())
            
        return None
    
    def get_defend_animation(self):
        if self.defend_image is not None:   
            if self.position == 'LEFT':
                return (self.defend_image, self.__where_is_shield())
            else:
                return (pygame.transform.flip(self.defend_image, True, False), self.__where_is_shield())
        return None
    
class Chicken(GameObject, pygame.sprite.Sprite):
    
    def __init__(self, position='LEFT'):
        
        self.path = './Characters/Chicken'
        self.race = 'chick'
        self.position = position
        
        self.egg_x_position, self.egg_y_position = self.initial_x_position, self.initial_y_position = self.x_position, self.y_position = CHICKEN_INIT_POSITION[position]['X'], CHICKEN_INIT_POSITION[position]['Y']
        if position == 'RIGHT':
            self.egg_x_position -= CHICKEN_EGG_WIDTH
            
        self.width, self.height = CHICKEN_WIDTH, CHICKEN_HEIGHT
        
        self.health, self.health_unit = 500, 50
        self.attack1_damage = random.randint(50, 60)
        self.attack2_damage = random.randint(60, 100)
        
        super().__init__()
        
class Dinosaur(GameObject, pygame.sprite.Sprite):
    
    def __init__(self, position='LEFT'):
        
        self.path = './Characters/Dinosaur'
        self.race = 'dino'
        self.position = position
        
        self.initial_x_position, self.initial_y_position = self.x_position, self.y_position = DINO_INIT_POSITION[position]['X'], DINO_INIT_POSITION[position]['Y']
        
        self.width, self.height = DINO_WIDTH, DINO_HEIGHT
        
        self.health, self.health_unit = 1000, 100
        self.attack1_damage = random.randint(20, 80)
        self.attack2_damage = random.randint(50, 120)        
        
        super().__init__()
        