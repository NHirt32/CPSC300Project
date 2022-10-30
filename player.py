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
                ["assets/5_1.png"],["assets/6_1.png"],
                ["assets/7_1.png","assets/7_2.png"],
                ["assets/8_1.png","assets/8_2.png"]],
                               pos)
        self.boing = 0  # Upward momentum.
        self.jump_power = 21  # Defines max jump power
        self.dive = 0  # Downward momentum
        self.gravity = 100  # Defines max fall speed
        self.slide_speed = 4 # defines gravity when sliding down a wall
        self.momentum = 0 # Used for non-wall jump related horizontal momentum
        self.speed = 15 # Max momentum. MUST BE EVENLY DIVISIBLE BY horizontal_acceleration
        self.horizontal_acceleration = 3
        self.wall_jump_cooldown = 20 # In frames of the game.
        self.wall_jump_cooldown_counter = 0 # Counter for cooldown
        self.wall_jump_horizontal_momentum = 21 # Max wall jump horizontal momentum. MUST BE EVENLY DIVISIBLE BY
        # horizontal_acceleration
        self.wall_jump_vertical_momentum = 21 # Max wall jump vertical momentum
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

        self.vertical_handler(x_direction, y_direction, collision_group, t_left, t_down, t_right, t_up)
        self.horizontal_handler(x_direction, collision_group, t_left, t_right)
        self.update_direction(x_direction, y_direction, collision_group, t_left, t_down, t_right, t_up)

    # Handles all horizontal movement relating to the player. Takes a collision group
    # and the horizontal input data as arguments.
    def horizontal_handler(self, x_mov, group, t_left, t_right):

        # Tests for right input, adjusts momentum by the acceleration if not touching a wall
        if (x_mov == 1) and (self.sign(self.momentum) >= 0):
            if not t_right:
                if (abs(self.momentum) <= self.speed):
                    self.momentum += self.horizontal_acceleration
            else:
                self.momentum = 0

        # Tests for left input, adjusts momentum by the acceleration if not touching a wall
        elif (x_mov == -1) and (self.sign(self.momentum) <= 0):
            if not t_left:
                if (abs(self.momentum) <= self.speed):
                    self.momentum -= self.horizontal_acceleration
            else:
                self.momentum = 0

        # If no input, then reduce momentum
        else:
            if self.momentum > 0:
                if (self.momentum != 0):
                    self.momentum -= self.horizontal_acceleration
            elif self.momentum < 0:
                if (self.momentum != 0):
                    self.momentum += self.horizontal_acceleration

        self.v_move_x(self.sign(self.momentum), abs(self.momentum), group)

    # Handles all vertical movement relating to the player. Takes a collision group
    # and the vertical input data as arguments.
    def vertical_handler(self,x_mov, y_mov, group, t_left, t_down, t_right, t_up):
        # Disables the autojump
        if self.can_jump:
            # Normal or walljump case detection.
            if (y_mov == -1) and t_down and (not t_up):  # -1 is up for y
                self.jump()

            # Detects if a walljump is possible
            elif (y_mov == -1) and (self.wall_jump_cooldown_counter == 0) and (not t_down) and (not t_up):
                # Detects a left wall jump
                if (not t_left) and t_right:
                    self.wall_jump_l()

                # Detects a right wall jump
                elif t_left and (not t_right):
                    self.wall_jump_r()

        # Checks if the player has let go of the jump key since the last jump.
        if y_mov == 0:
            self.can_jump = True

        # Processing the boing of a jump
        if (self.boing != 0) and (not t_up):
            self.v_move_y(-1, self.boing, group)
            self.boing -= 1
        else:
            self.boing = 0

        # Dealing with the player cooldown
        if self.wall_jump_cooldown_counter != 0:
            self.wall_jump_cooldown_counter -= 1

        #Process gravity
        self.gravity_handler(x_mov,group)

    # Does mostly horizontal movement, but needs to factor in when sliding and when not sliding.
    def gravity_handler(self, x_mov, group):
        # If sliding
        if ((self.touching_right(group) and (x_mov == 1)) or (self.touching_left(group) and (x_mov == -1))) and\
            (not self.touching_ground(group)):
            if self.boing == 0:
                self.v_move_y(1, self.dive, group)
                if (self.dive <= self.slide_speed):
                    self.dive += 1
                else:
                    self.dive -= 1
            else:
                self.dive = 0

        # if falling
        else:
            # Processing the dive of the player falling
            if (self.boing == 0) and (not (self.touching_ground(group))):
                self.v_move_y(1, self.dive, group)
                if (self.dive != self.gravity):
                    self.dive += 1
            else:
                self.dive = 0

    # Updates the player's direction variable, which controls which animations are shown.
    def update_direction(self, x_mov, y_mov, group, t_left, t_down, t_right, t_up):

        m_direction = self.sign(self.momentum)
        if (x_mov == 0) and t_down and (m_direction == 1):
            self.direction = self.STANDING_STILL_RIGHT
        elif(x_mov == 0) and t_down and (m_direction == -1):
            self.direction = self.STANDING_STILL_LEFT
        elif (x_mov == 1) and t_down and (m_direction == 1):
            self.direction = self.WALKING_RIGHT
        elif (x_mov == -1) and t_down and (m_direction == -1):
            self.direction = self.WALKING_LEFT
        elif (x_mov == -1) and t_down and (m_direction == 1):
            self.direction = self.WALKING_LEFT
        elif (x_mov == 1) and t_down and (m_direction == -1):
            self.direction = self.WALKING_RIGHT


    # Checks if the player collided with the passed group. This should
    # not be a group that collisions are forbidden with by move_y(), move_x() and v_mov_y()
    def collided_with(self, group):
        if pygame.sprite.spritecollideany(self, group) != None:
            return True

    def jump(self):
        self.boing = self.jump_power
        self.can_jump = False

    # Makes conditions right for the player to wall jump left
    def wall_jump_l(self):
        self.boing = self.wall_jump_vertical_momentum
        self.momentum = -1 * self.wall_jump_horizontal_momentum
        self.wall_jump_cooldown_counter = self.wall_jump_cooldown
        self.can_jump = False

    # Makes conditions right for the player to wall jump right
    def wall_jump_r(self):
        self.boing = self.wall_jump_vertical_momentum
        self.momentum = self.wall_jump_horizontal_momentum
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

