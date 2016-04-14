import pygame
 
class Spritesheet():
    def __init__(self, path):
        self.sheet = pygame.image.load(path).convert_alpha()

    def get_image(self, rectangle, colorkey = None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size, pygame.SRCALPHA)
        image.fill((0,0,0,0))
        image.blit(self.sheet, (0, 0), rectangle)
        
        return image