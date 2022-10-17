import pygame
import tile
import settings


class Animation(tile.Tile):
    def __init__(self, frames, pos):
        tile.Tile.__init__(self, frames[0][0], pos)
        self.frames = frames
        self.current_frame = 0

        # Direction refers to which animation set should be accessed.
        # For example, if a player moves right, a different set of images should be used than if a player
        # were to have moved left. Thus, take care to define direction appropriately, and initialize
        # animations with file paths in measurable orders
        self.direction = 0

    # Flips to the next frame of the specified direction
    def next(self, direction):

        if direction == self.direction:
            self.image = pygame.image.load(self.frames[self.direction][self.current_frame])
            if (self.current_frame < (len(self.frames[self.direction]) - 1)):
                self.current_frame += 1
            else:
                self.current_frame = 0

        else:
            self.current_frame = 0
            self.direction = direction
            self.image = pygame.image.load(self.frames[direction][self.current_frame])
            if (self.current_frame < (len(self.frames[self.direction]) - 1)):
                self.current_frame += 1
            else:
                self.current_frame = 0
