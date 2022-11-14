import pygame
import tile
import settings


class Animation(tile.Tile):
    def __init__(self, images, pos):
        tile.Tile.__init__(self, images[0][0], pos)
        self.current_frame = 0
        self.frames = [[]]

        # Load all images in at start, not constantly from the disc.
        # Store it with the player, so its easily retrieved and switched.
        for i in range(0, len(images)):
            self.frames.append([])
            for j in range(0, len(images[i])):
                self.frames[i].append(pygame.image.load(images[i][j]).convert_alpha())

        # Direction refers to which animation set should be accessed.
        # For example, if a player moves right, a different set of images should be used than if a player
        # were to have moved left. Thus, take care to define direction appropriately, and initialize
        # animations with file paths in measurable orders
        # Need to record the direction of the previous frame for comparisons about the next frame.
        self.direction = 0

        # May be changed due to some event, like player input or entity collision.
        # The direction will change to next direction.
        self.next_direction = 0

    # Flips to the next frame of the specified direction
    def next(self):

        length = len(self.frames[self.direction])

        if self.next_direction == self.direction:
            self.image = self.frames[self.direction][self.current_frame]
            self.current_frame += 1
            if not (self.current_frame < length):
                self.current_frame = 0

        else:
            self.current_frame = 0
            self.direction = self.next_direction
            self.image = self.frames[self.direction][self.current_frame]
            self.current_frame += 1
            if not (self.current_frame < length):
                self.current_frame = 0
