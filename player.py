import pygame
import tile
import entity
from settings import *
import math

class Player(entity.Entity):
    def __init__(self, pos):
        entity.Entity.__init__(self,
                [["assets/1_1.png","assets/1_2.png","assets/1_3.png","assets/1_2.png","assets/1_1.png"],
                ["assets/2_1.png","assets/2_2.png","assets/2_3.png","assets/2_2.png","assets/2_1.png"],
                ["assets/3_1.png","assets/1_1.png","assets/3_2.png","assets/1_1.png"],
                ["assets/4_2.png","assets/2_1.png","assets/4_1.png","assets/2_1.png"],
                ["assets/5_1.png","assets/5_1.png","assets/5_1.png"],
                ["assets/6_1.png","assets/6_1.png","assets/6_1.png"],
                ["assets/7_1.png","assets/7_2.png"],
                ["assets/8_1.png","assets/8_2.png"]],
                               pos)
        self.jump_power = 21  # Defines max jump power
        self.gravity = 40  # Defines max fall speed.
        self.slide_speed = 4  # defines gravity when sliding down a wall
        self.vertical_momentum = 0
        self.horizontal_momentum = 0  # Used for non-wall jump related horizontal momentum
        self.speed = 12  # Max momentum. MUST BE EVENLY DIVISIBLE BY horizontal_acceleration
        self.horizontal_acceleration = 3
        self.wall_jump_cooldown = 20  # In frames of the game.
        self.wall_jump_cooldown_counter = 0  # Counter for cooldown
        self.wall_jump_horizontal_momentum = 21  # Max wall jump horizontal momentum. MUST BE EVENLY DIVISIBLE BY
        # horizontal_acceleration
        self.wall_jump_vertical_momentum = 21  # Max wall jump vertical momentum
        self.can_jump = True

        # Directions
        self.STANDING_STILL_LEFT = 1
        self.STANDING_STILL_RIGHT = 0
        self.WALKING_RIGHT = 2
        self.WALKING_LEFT = 3
        self.JUMPING_LEFT = 5
        self.JUMPING_RIGHT = 4
        self.SLIDING_LEFT = 7
        self.SLIDING_RIGHT = 6

    # Does all the movement associated with the player
    def update(self, x_direction, y_direction, collision_group):
        t_left = self.touching_left(collision_group)
        t_down = self.touching_ground(collision_group)
        t_right = self.touching_right(collision_group)
        t_up = self.touching_roof(collision_group)

        # Disables the autojump
        if self.can_jump:
            # Normal or walljump case detection.
            if (y_direction == -1) and t_down and (not t_up):  # -1 is up for y
                self.jump()

            # Detects if a walljump is possible
            elif (y_direction == -1) and (self.wall_jump_cooldown_counter == 0) and (not t_down) and (not t_up):
                # Detects a left wall jump
                if (not t_left) and t_right:
                    self.wall_jump_l()

                # Detects a right wall jump
                elif t_left and (not t_right):
                    self.wall_jump_r()

        # Checks if the player has let go of the jump key since the last jump.
        if y_direction == 0:
            self.can_jump = True

        self.vertical_handler(x_direction, collision_group, t_up)
        self.horizontal_handler(x_direction, collision_group, t_left, t_right)
        self.update_direction(x_direction, y_direction, collision_group, t_left, t_down, t_right, t_up)

    # Handles all horizontal movement relating to the player. Takes a collision group
    # and the horizontal input data as arguments.
    def horizontal_handler(self, x_mov, group, t_left, t_right):

        # Tests for right input, adjusts momentum by the acceleration if not touching a wall
        if (x_mov == 1) and (self.sign(self.horizontal_momentum) >= 0):
            if not t_right:
                if (abs(self.horizontal_momentum) <= self.speed):
                    self.horizontal_momentum += self.horizontal_acceleration
            else:
                self.horizontal_momentum = 0

        # Tests for left input, adjusts momentum by the acceleration if not touching a wall
        elif (x_mov == -1) and (self.sign(self.horizontal_momentum) <= 0):
            if not t_left:
                if (abs(self.horizontal_momentum) <= self.speed):
                    self.horizontal_momentum -= self.horizontal_acceleration
            else:
                self.horizontal_momentum = 0

        # If no input, then reduce momentum
        else:
            if self.horizontal_momentum > 0:
                if (self.horizontal_momentum != 0):
                    self.horizontal_momentum -= self.horizontal_acceleration
            elif self.horizontal_momentum < 0:
                if (self.horizontal_momentum != 0):
                    self.horizontal_momentum += self.horizontal_acceleration

        self.v_move_x(self.sign(self.horizontal_momentum), abs(self.horizontal_momentum), group)

    # Handles all vertical movement relating to the player. Takes a collision group
    # and the vertical input data as arguments.
    def vertical_handler(self,x_mov, group, t_up):

        # Processing upward vertical momentum, like in the case of jump.
        if (self.vertical_momentum > 0) and (not t_up):
            self.v_move_y(-1, self.vertical_momentum, group)
            self.vertical_momentum -= 1

        # Makes sure that the player bounces off the roof, and does not stick to it.
        if t_up:
            self.vertical_momentum = -1

        # Dealing with the player cooldown
        if self.wall_jump_cooldown_counter != 0:
            self.wall_jump_cooldown_counter -= 1

        #Process downward vertical momentum
        self.gravity_handler(x_mov,group)

    # Does mostly downward vertical movement, but needs to factor in when sliding and when not sliding.
    def gravity_handler(self, x_mov, group):
        # If sliding
        if ((self.touching_right(group) and (x_mov == 1)) or (self.touching_left(group) and (x_mov == -1))) and\
            (not self.touching_ground(group)):
            if self.vertical_momentum <= 0:
                self.v_move_y(1, abs(self.vertical_momentum), group)
                if (abs(self.vertical_momentum) <= self.slide_speed):
                    self.vertical_momentum -= 1
                else:
                    self.vertical_momentum += 1

        # if falling
        elif(not self.touching_ground(group)):
            if self.vertical_momentum <= 0:
                self.v_move_y(1, abs(self.vertical_momentum), group)
                if (self.vertical_momentum <= self.gravity):
                    self.vertical_momentum -= 1
                else:
                    self.vertical_momentum += 1

        else:
            self.vertical_momentum = 0

    # Updates the player's direction variable, which controls which animations are shown.
    def update_direction(self, x_mov, y_mov, group, t_left, t_down, t_right, t_up):

        m_direction = self.sign(self.horizontal_momentum)
        if t_down:
            if m_direction != 0:
                if m_direction == 1:
                    if x_mov == 1:
                        self.next_direction = self.WALKING_RIGHT
                    else:
                        self.next_direction = self.STANDING_STILL_RIGHT
                elif m_direction == -1:
                    if x_mov == -1:
                        self.next_direction = self.WALKING_LEFT
                    else:
                        self.next_direction = self.STANDING_STILL_LEFT
            else:
                self.next_direction = self.direction

        elif (not t_down) and self.vertical_momentum < 1:
            if (self.direction == self.STANDING_STILL_LEFT) or (self.direction == self.WALKING_LEFT) \
                or (self.direction == self.SLIDING_LEFT):
                self.next_direction = self.STANDING_STILL_LEFT
            elif (self.direction == self.STANDING_STILL_RIGHT) or (self.direction == self.WALKING_RIGHT) \
                or (self.direction == self.SLIDING_RIGHT):
                self.next_direction = self.SLIDING_RIGHT
        elif (not t_down) and self.vertical_momentum >= 1:
            if (self.direction == self.STANDING_STILL_LEFT) or (self.direction == self.WALKING_LEFT):
                self.next_direction = self.JUMPING_LEFT
            elif (self.direction == self.STANDING_STILL_RIGHT) or (self.direction == self.WALKING_RIGHT):
                self.next_direction = self.JUMPING_RIGHT

    def jump(self):
        self.vertical_momentum = self.jump_power
        self.can_jump = False

    # Makes conditions right for the player to wall jump left
    def wall_jump_l(self):
        self.vertical_momentum = self.wall_jump_vertical_momentum
        self.horizontal_momentum = -1 * self.wall_jump_horizontal_momentum
        self.wall_jump_cooldown_counter = self.wall_jump_cooldown
        self.can_jump = False

    # Makes conditions right for the player to wall jump right
    def wall_jump_r(self):
        self.vertical_momentum = self.wall_jump_vertical_momentum
        self.horizontal_momentum = self.wall_jump_horizontal_momentum
        self.wall_jump_cooldown_counter = self.wall_jump_cooldown
        self.can_jump = False

    # Takes a number. Returns -1 if the number is negative, 0 if its 0, and 1 if its positive
    def sign(self, number):
        if number > 0:
            return 1
        elif number == 0:
            return 0
        elif number < 0:
            return -1