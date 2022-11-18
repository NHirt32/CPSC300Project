import pygame
import enemy #Inherits functionality from enemy

class walker(enemy.Enemy):

    def __init__(self, pos):
        enemy.Enemy.__init__(self, [["assets/red_player.png"]], pos)
        self.gravity = -100  # Defines max fall speed, must be negative
        self.vertical_momentum = 0

    # Does mostly downward vertical movement, but needs to factor in when sliding and when not sliding.
    def gravity_handler(self, group):
        # if falling
        if (not self.touching_ground(group)):
            if self.vertical_momentum <= 0:
                self.v_move_y(1, abs(self.vertical_momentum), group)
                if (self.vertical_momentum < self.gravity):
                    self.vertical_momentum += 1
                else:
                    self.vertical_momentum -= 1

    def update(self, group):
        if (self.edge_detect(group) == False): # If the enemy is not colliding with a solid
            self.move_x(self.move_int, group)
        else: # If the enemy is colliding with a solid
            self.move_int *= -1 # Turn around
            self.move_x(self.move_int, group) # Move slightly to avoid being stuck on the wall

        # Primitive enemy gravity handling.
        self.gravity_handler(group)

