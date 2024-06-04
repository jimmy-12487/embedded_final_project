import pygame
from pygame.locals import *

class playing_scene:
    def __init__(self, roles):
        self.roles = roles
        pass
    
    def update(self):
        for role in self.roles:
            role.update()
    
    def action_collect(self, main_scene):
        for event in pygame.event.get():
            if event.type == QUIT:
                return None
            
            if event.type != KEYDOWN:
                continue
            
            e = event.dict['key']
            
        return False
    
    def get_objects(self):
        objects = []
        for role in self.roles:
            if role.is_left:
                objects += [(role.main_image, role.main_rect), (role.health_image, role.health_rect), (role.health_icon_image, role.health_icon_rect)]
            else:
                objects +=[(pygame.transform.flip(role.main_image, True, False), role.main_rect),
                           (pygame.transform.flip(role.health_image, True, False), role.health_rect),
                           (pygame.transform.flip(role.health_icon_image, True, False), role.health_icon_rect)
                           ]
            
        return objects
        