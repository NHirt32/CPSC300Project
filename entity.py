import pygame
import tile
import animation
from settings import *

class Entity(animation.Animation):
    # frames is a list of lists of strings. The strings are filepaths, each list of strings is an animation set
    def __init__(self, frames, pos):
        animation.Animation.__init__(self, frames, pos)
        self.speed = 10

    # Checks if the entity is touching the passed group beneath the entity.
    def touching_ground(self, group):
        self.rect.y += 1
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.y -= 1
            return True
        else:
            self.rect.y -= 1
            return False

    # Checks if the entity is touching the passed group to the right of the entity.
    def touching_right(self, group):
        self.rect.x += 1
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.x -= 1
            return True
        else:
            self.rect.x -= 1
            return False

    # Checks if the entity is touching the passed group to the left of the entity.
    def touching_left(self, group):
        self.rect.x -= 1
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.x += 1
            return True
        else:
            self.rect.x += 1
            return False

    # Checks if the entity is touching the passed group above the entity.
    def touching_roof(self, group):
        self.rect.y -= 1
        if pygame.sprite.spritecollideany(self, group) != None:
            self.rect.y += 1
            return True
        else:
            self.rect.y -= 1
            return False

    # Checks if the entity collided with the passed group. This should
    # not be a group that collisions are forbidden with by move_y(), move_x() and v_mov_y()
    def collided_with(self, group):
        if pygame.sprite.spritecollideany(self, group) != None:
            return True

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