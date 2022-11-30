import pygame
import animation

class Entity(animation.Animation):
    """The Entity class extends an animation with the basic functionality all entities should have, like
    movement and collision detection."""
    def __init__(self, frames, pos):
        """Constructor for an Entity.

        :param frames: a list of lists of strings that are filepaths to images.
        :param pos: a position as a tuple."""
        animation.Animation.__init__(self, frames, pos)
        self.speed = 10

    def touching_ground(self, group):
        """touching_ground() returns whether the entity is touching a sprite below itself.

        :param group: the passed group to test for collisions.
        :returns: true if the entity is touching a sprite below itself."""
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, group) != None: # If the entity is 1 pixel from touching a floor
            self.rect.y -= 1
            return True
        else: # If the entity is not 1 pixel from touching a floor
            self.rect.y -= 1
            return False

    def touching_right(self, group):
        """touching_right() returns whether the entity is touching a sprite to the entity's right.

        :param group: the passed group to test for collisions.
        :returns: true if the entity is touching a sprite to the entity's right."""
        self.rect.x += 1
        if pygame.sprite.spritecollideany(self, group) != None: # If the entity is 1 pixel from touching a wall on the right
            self.rect.x -= 1
            return True
        else:   # If entity is not 1 pixel from touching a wall on the right
            self.rect.x -= 1
            return False


    def touching_left(self, group):
        """touching_left() returns whether the entity is touching a sprite to the entity's left.

        :param group: the passed group to test for collisions.
        :returns: true if the entity is touching a sprite to the entity's left."""
        self.rect.x -= 1
        if pygame.sprite.spritecollideany(self, group) != None: # If the entity is 1 pixel from touching a wall on the left
            self.rect.x += 1
            return True
        else:   # If the entity is not 1 pixel from touching a wall on the left
            self.rect.x += 1
            return False


    def touching_roof(self, group):
        """touching_roof() returns whether the entity is touching a sprite above the entity.

        :param group: the passed group to test for collisions.
        :returns: true if the entity is touching a sprite above the entity."""
        self.rect.y -= 1
        if pygame.sprite.spritecollideany(self, group) != None: # If the entity is 1 pixel from touching a ceiling
            self.rect.y += 1
            return True
        else:   # If the entity is not 1 pixel from touching a ceiling
            self.rect.y += 1
            return False

    def move_x(self, x_pos, group):
        """move_x() tries to move an entity horizontally based on its speed, it will not allow collision.

        :param x_pos: the direction to move.
        :param group: the group for disallowing collisions."""
        self.rect.x += x_pos * self.speed
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.x -= x_pos * self.speed
            while pygame.sprite.spritecollideany(self, group) == None:
                self.rect.x += x_pos
            self.rect.x -= x_pos

    def move_y(self, y_pos, group):
        """move_y() tries to move an entity vertically based on its speed, it will not allow collision.

        :param y_pos: the direction to move.
        :param group: the group for disallowing collisions."""
        self.rect.y += y_pos * self.speed
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.y -= y_pos * self.speed
            while pygame.sprite.spritecollideany(self, group) == None:
                self.rect.y += y_pos
            self.rect.y -= y_pos

    def v_move_y(self, y_pos, speed, group):
        """v_move_y() tries to move an entity vertically based on a speed, it will not allow collision.

        :param y_pos: the direction to move.
        :param speed: the number of pixels to move the entity.
        :param group: the group for disallowing collisions."""
        self.rect.y += y_pos * speed
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.y -= y_pos * speed
            while pygame.sprite.spritecollideany(self, group) == None:
                self.rect.y += y_pos
            self.rect.y -= y_pos

    def v_move_x(self, x_pos, speed, group):
        """v_move_x() tries to move an entity horizontally based on a speed, it will not allow collision.

        :param x_pos: the direction to move.
        :param speed: the number of pixels to move the entity.
        :param group: the group for disallowing collisions."""
        self.rect.x += x_pos * speed
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.x -= x_pos * speed
            while pygame.sprite.spritecollideany(self, group) == None:
                self.rect.x += x_pos
            self.rect.x -= x_pos

    def collided_with(self, group):
        """collided_with() returns whether the entity collided with a sprite in a group.

        :param group: the group to test for collision.
        :returns: true if the entity collided with a sprite in a group."""
        if pygame.sprite.spritecollideany(self, group) != None:
            return True