import pygame
from pygame.locals import *
from enums import *

class playing_scene:
    def __init__(self, roles):
        self.roles = roles
        pass
    
    def update(self):
        self.roles[0].update(self.roles[1])
        self.roles[1].update(self.roles[0])
    
    def interaction_arbitration(self):
        # self.roles[0].interaction(self.roles[1])
        # self.roles[1].interaction(self.roles[0])
        
        pass
    
    def action_collect(self, main_scene):
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            
            if event.type != KEYDOWN:
                continue
            
            e = event.dict['key']
            
            if e == K_a:
                self.roles[0].user_input = {'state': STATES.FORWARD, 
                                            'direction': DIRECTION.RIGHT, 
                                            'attack_movement': ATTACK_MOVEMENT.ATTACK2 }
            elif e == K_d:
                self.roles[0].user_input = {'state': STATES.ATTACK, 
                                            'direction': DIRECTION.STILL, 
                                            'attack_movement': ATTACK_MOVEMENT.ATTACK1 }
            elif e == K_w:
                self.roles[0].user_input = {'state': STATES.IDLE, 
                                            'direction': DIRECTION.STILL, 
                                            'attack_movement': ATTACK_MOVEMENT.NONE }  
            elif e == K_s:
                self.roles[0].health -= 5
                
            elif e == K_LEFT:
                self.roles[1].user_input = {'state': STATES.FORWARD, 
                                            'direction': DIRECTION.LEFT, 
                                            'attack_movement': ATTACK_MOVEMENT.ATTACK2 }
            elif e == K_RIGHT:
                self.roles[1].user_input = {'state': STATES.ATTACK, 
                                            'direction': DIRECTION.STILL, 
                                            'attack_movement': ATTACK_MOVEMENT.ATTACK1 }
            elif e == K_UP:
                self.roles[1].user_input = {'state': STATES.IDLE, 
                                            'direction': DIRECTION.STILL, 
                                            'attack_movement': ATTACK_MOVEMENT.NONE } 
            elif e == K_DOWN:
                self.roles[1].health -= 5
            
            if self.roles[0].health <= 0:
                self.roles[0].next_state = STATES.DIE
            if self.roles[1].health <= 0:
                self.roles[1].next_state = STATES.DIE
            if self.roles[0].state == STATES.DIE:
                self.roles[0].next_state = STATES.DIE
            if self.roles[1].state == STATES.DIE:
                self.roles[1].next_state = STATES.DIE
        self.interaction_arbitration()
        return False
    
    def get_objects(self):
        objects = []
        for role in self.roles:
            objects += role.get_objects()
            
        return objects
        