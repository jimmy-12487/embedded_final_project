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
                self.roles[0].user_input = {'state': STATES.DEFENDING, 
                                            'direction': DIRECTION.STILL, 
                                            'attack_movement': ATTACK_MOVEMENT.NONE } 
                
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
                self.roles[1].user_input = {'state': STATES.DEFENDING, 
                                            'direction': DIRECTION.STILL, 
                                            'attack_movement': ATTACK_MOVEMENT.NONE } 
        
        for v in main_scene.user_input.values():
            dir = DIRECTION.RIGHT if v['index'] == 0 else DIRECTION.LEFT
            if v['input'] == VOICE.DEFEND:
                self.roles[v['index']].user_input = {
                    'state': STATES.DEFENDING, 
                    'direction': DIRECTION.STILL, 
                    'attack_movement': ATTACK_MOVEMENT.NONE,
                    'volumn': v['volumn']
                } 
            elif v['input'] == VOICE.ATTACK1:
                self.roles[v['index']].user_input = {
                    'state': STATES.ATTACK, 
                    'direction': DIRECTION.STILL, 
                    'attack_movement': ATTACK_MOVEMENT.ATTACK1,
                    'volumn': v['volumn']
                }
            elif v['input'] == VOICE.ATTACK2:
                self.roles[v['index']].user_input = {
                    'state': STATES.FORWARD, 
                    'direction': dir, 
                    'attack_movement': ATTACK_MOVEMENT.ATTACK2,
                    'volumn': v['volumn']
                }
            else:
                self.roles[v['index']].user_input = {}
            v['input'] = ''
        return False
    
    def get_objects(self):
        objects = []
        for role in self.roles:
            objects += role.get_objects()
        for role in self.roles:
            attack = role.get_attack_animation()
            defend = role.get_defend_animation()
            if attack is not None:
                objects.append(attack)
            if defend is not None:
                objects.append(defend)
                
        return objects
        