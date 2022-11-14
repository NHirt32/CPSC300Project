import pygame
import tile
import animation
from settings import *  

class Entity(animation.Animation):
    # frames is a list of lists of strings. The strings are filepaths, each list of strings is an animation set
    def __init__(self, frames, pos):
        animation.Animation.__init__(self, frames, pos)
        self.speed = 10
        self.gravity = 100  # Defines max fall speed, must be negative.
        self.vertical_momentum = 0

    # Checks if the entity is touching the passed group beneath the entity.
    def touching_ground(self, group):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, group) != None: # If the entity is 1 pixel from touching a floor
            self.rect.y -= 1
            return True
        else: # If the entity is not 1 pixel from touching a floor
            self.rect.y -= 1
            return False

    # Checks if the entity is touching the passed group to the right of the entity.
    def touching_right(self, group):
        self.rect.x += 1
        if pygame.sprite.spritecollideany(self, group) != None: # If the entity is 1 pixel from touching a wall on the right
            self.rect.x -= 1
            return True
        else:   # If entity is not 1 pixel from touching a wall on the right
            self.rect.x -= 1
            return False

    # Checks if the entity is touching the passed group to the left of the entity.
    def touching_left(self, group):
        self.rect.x -= 1
        if pygame.sprite.spritecollideany(self, group) != None: # If the entity is 1 pixel from touching a wall on the left
            self.rect.x += 1
            return True
        else:   # If the entity is not 1 pixel from touching a wall on the left
            self.rect.x += 1
            return False

    # Checks if the entity is touching the passed group above the entity.
    def touching_roof(self, group):
        self.rect.y -= 1
        if pygame.sprite.spritecollideany(self, group) != None: # If the entity is 1 pixel from touching a ceiling
            self.rect.y += 1
            return True
        else:   # If the entity is not 1 pixel from touching a ceiling
            self.rect.y += 1
            return False

    # Tries to move entity horizontally and already factors in entity speed.
    # Disables collision with the passed group.
    def move_x(self, x_pos, group):
        self.rect.x += x_pos * self.speed
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.x -= x_pos * self.speed
            while pygame.sprite.spritecollideany(self, group) == None:
                self.rect.x += x_pos
            self.rect.x -= x_pos

    # Tries to move entity vertically and factors in entity speed.
    # Disables collision with the passed group.
    def move_y(self, y_pos, group):
        self.rect.y += y_pos * self.speed
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.y -= y_pos * self.speed
            while pygame.sprite.spritecollideany(self, group) == None:
                self.rect.y += y_pos
            self.rect.y -= y_pos

    # Tries to move entity vertically and factors in the speed argument.
    # Disables collision with the passed group.
    def v_move_y(self, y_pos, speed, group):
        self.rect.y += y_pos * speed
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.y -= y_pos * speed
            while pygame.sprite.spritecollideany(self, group) == None:
                self.rect.y += y_pos
            self.rect.y -= y_pos

    # Tries to move entity vertically and factors in the speed argument.
    # Disables collision with the passed group.
    def v_move_x(self, x_pos, speed, group):
        self.rect.x += x_pos * speed
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.x -= x_pos * speed
            while pygame.sprite.spritecollideany(self, group) == None:
                self.rect.x += x_pos
            self.rect.x -= x_pos

    def vertical_handler(self,x_mov, group, t_up):

        # Processing upward vertical momentum, like in the case of jump.
        if (self.vertical_momentum > 0) and (not t_up):
            self.v_move_y(-1, self.vertical_momentum, group)
            self.vertical_momentum -= 1

        # Makes sure that the player bounces off the roof, and does not stick to it.
        if t_up:
            self.vertical_momentum = -1

        #Process downward vertical momentum
        self.gravity_handler(group)

    # Does mostly downward vertical movement, but needs to factor in when sliding and when not sliding.
    def gravity_handler(self, group):
        # if falling
        if(not self.touching_ground(group)):
            if self.vertical_momentum <= 0:
                self.v_move_y(1, abs(self.vertical_momentum), group)
                if (self.vertical_momentum <= self.gravity):
                    self.vertical_momentum -= 1
                else:
                    self.vertical_momentum += 1

    # Checks if the entity collided with the passed group. This should
    # not be a group that collisions are forbidden with by move_y(), move_x() and v_mov_y()
    def collided_with(self, group):
        if pygame.sprite.spritecollideany(self, group) != None:
            return True