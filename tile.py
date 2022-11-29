import pygame
from settings import *


class Tile(pygame.sprite.Sprite):
    """The Tile class extends sprite to give the functionality tiles should have.
    This is basically just making sure sprites are rendered from the midbottom position."""
    def __init__(self, image, pos):
        """Constructor for an Tile.

        :param image: a string of the file path for an image.
        :param pos: a position as a tuple."""
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image).convert_alpha()
        # Important thing here is basically everything is placed from the top left by the renderer.
        self.rect = self.image.get_rect(midbottom=pos)

