import pygame
import tile
import entity
from settings import *


class Player(entity.Entity):
    def __init__(self, pos):
        entity.Entity.__init__(self, [["assets/player.png", "assets/red_player.png"]], pos)
        self.speed = 10
        self.boing = 0  # Also known as upward momentum.
        self.dive = 0  # downward momentum
        self.right_momentum = 0
        self.left_momentum = 0
        self.gravity = 100  # defines max fall speed
        self.jump_power = 20  # defines max jump power
        self.can_jump = True
        self.wall_jump_cooldown = 30 # In frames of the game.

    # Does all the movement associated with the player
    def update(self, x_direction, y_direction, collision_group):
        self.move_x(x_direction, collision_group)
        self.jump(y_direction, collision_group)
        self.fall(collision_group)

    # Uses the passed input to determine if a jump, or walljump, should occur, handles the cooldown associated
    # with a walljump, and actually does the jump.
    def jump(self, y_mov, group):

        # Normal jump from the ground case detection
        if y_mov == -1 and self.touching_ground(group):  # -1 is up for y
            self.boing = self.jump_power

        # Wall jump case detection
        elif y_mov == -1 and (self.touching_left(group) or self.touching_right(group)) and \
                (self.wall_jump_cooldown == 0) and not \
                self.touching_ground(group):
            self.boing = self.jump_power
            self.wall_jump_cooldown = 30

        # Actually processing a jump
        if self.boing != 0 and not (self.touching_roof(group)):
            self.v_move_y(-1, self.boing, group)
            self.boing -= 1
        else:
            self.boing = 0

        # Dealing with the player cooldown
        if self.wall_jump_cooldown != 0:
            self.wall_jump_cooldown -= 1

    # Applies downward shift if momentum has run out, basically speeding up gravity to a point.
    def fall(self, group):
        if self.boing == 0 and not (self.touching_ground(group)):
            self.v_move_y(1, self.dive, group)
            if (self.dive != self.gravity):
                self.dive += 1
        else:
            self.dive = 0

    # Checks if the player collided with the passed group. This should
    # not be a group that collisions are forbidden with by move_y(), move_x() and v_mov_y()
    def collided_with(self, group):
        if pygame.sprite.spritecollideany(self, group) != None:
            return True
