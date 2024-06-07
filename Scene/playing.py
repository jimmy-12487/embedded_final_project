import pygame
from pygame.locals import *
from enums import *

class playing_scene:
    def __init__(self, roles):
        self.roles = roles
        pass
    
    def update(self):
        for role in self.roles:
            role.update()
    
    # def interaction_arbitration(self):
        
    
    def action_collect(self, main_scene):
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            
            if event.type != KEYDOWN:
                continue
            
            e = event.dict['key']
            
            if e == K_d:
                self.roles[0].next_state = STATES.ATTACK
                self.roles[0].next_attack_state = ATTACK_MOVEMENT.ATTACK1
            elif e == K_w:
                self.roles[0].health += 5
            elif e == K_s:
                self.roles[0].health -= 5
                
            elif e == K_RIGHT:
                self.roles[1].next_state = STATES.ATTACK
                self.roles[1].next_attack_state = ATTACK_MOVEMENT.ATTACK1
            elif e == K_UP:
                self.roles[1].health += 5
            elif e == K_DOWN:
                self.roles[1].health -= 5
            
            if self.roles[0].health <= 11:
                self.roles[0].next_state = STATES.DIE
            if self.roles[1].health <= 11:
                self.roles[1].next_state = STATES.DIE
            if self.roles[0].state == STATES.DIE:
                self.roles[0].next_state = STATES.DIE
            if self.roles[1].state == STATES.DIE:
                self.roles[1].next_state = STATES.DIE
            
        return False
    
    def get_objects(self):
        objects = []
        for role in self.roles:
            objects += role.get_objects()
            
        return objects
        