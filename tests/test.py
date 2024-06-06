import pygame
pygame.init()
surface = pygame.display.set_mode((1200, 800))
img = './Characters/Dinosaur/attack1_0.png'

image = pygame.transform.flip(
            pygame.image.load(img).convert_alpha(), True, False)

pygame.image.save(image, './flipped.png')