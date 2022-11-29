import pygame
import tile

class Animation(tile.Tile):
    """The Animation class extends a tile by adding multiple frames, and has the functionality to change to
    the next frame in a list or a new list of frames. To change the list of frames an animation is iterating over,
    change the next_direction field."""

    def __init__(self, images, pos):
        """Constructor for an Animation.

        :param images: a list of lists of strings that are filepaths to images.
        :param pos: a position as a tuple."""
        tile.Tile.__init__(self, images[0][0], pos)
        self.current_frame = 0
        self.frames = [[]]

        # Load all images in at start, not constantly from the disc.
        # Store it with the animation, so its easily retrieved and switched.
        for i in range(0, len(images)):
            self.frames.append([])
            for j in range(0, len(images[i])):
                self.frames[i].append(pygame.image.load(images[i][j]).convert_alpha())

        # Direction refers to which animation set should be accessed.
        # For example, if a player moves right, a different set of images should be used than if a player
        # were to have moved left. Thus, take care to define direction appropriately, and initialize
        # animations with file paths in measurable orders.
        # Need to record the direction of the previous frame for comparisons about the next frame.
        self.direction = 0

        # May be changed due to some event, like player input or entity collision.
        # The direction will change to next direction.
        self.next_direction = 0

    def next(self):
        """next() will make the animation display the next frame in the list, or reset to the start of the list if it
        has reached the end."""

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
