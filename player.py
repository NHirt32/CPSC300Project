import pygame
import tile
import entity
from settings import *

class Player(entity.Entity):
    def __init__(self, pos):
        entity.Entity.__init__(self, [["assets/player.png","assets/red_player.png"]], pos)
        self.speed = 10
        self.boing = 0 # Also known as upward momentum.
        self.dive = 0 # downward momentum
        self.right_momentum = 0
        self.left_momentum = 0
        self.gravity = 100 # defines max fall speed
        self.jump_power = 20 #defines max jump power

    # Applies upward shift if the player still has momentum, basically speeding up the jump to a point.
    # Resets momentum if a roof is hit.
    def jump(self, group):
        if self.boing != 0 and not(self.touching_roof(group)):
            self.v_move_y(-1, self.boing, group)
            self.boing -= 1
        else:
            self.boing = 0

    # Applies downward shift if momentum has run out, basically speeding up gravity to a point.
    def fall(self, group):
        if self.boing == 0 and not(self.touching_ground(group)):
            self.v_move_y(1, self.dive, group)
            if(self.dive != self.gravity):
                self.dive += 1
        else:
            self.dive = 0

    # Checks if the player collided with the passed group. This should
    # not be a group that collisions are forbidden with by move_y(), move_x() and v_mov_y()
    def collided_with(self, group):
        if pygame.sprite.spritecollideany(self, group) != None:
            return True