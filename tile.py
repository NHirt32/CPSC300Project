import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    def __init__(self, image, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        # Important thing here is basically everything is placed from the top left by the renderer.
        self.rect = self.image.get_rect(topleft=pos)
